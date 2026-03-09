#!/usr/bin/env python3
"""
=============================================================
  PROSPECTION AUTONOME — Studio Riad
  Module importable par Flask + usage CLI conservé
=============================================================
CLI Usage:
  python3 prospection.py --day 3 --test
  python3 prospection.py --day 3 --count 10
Module Usage:
  from prospection import run_day
  result = run_day("3", count=10, geo_zone="bretagne", log_cb=print)
=============================================================
"""

import os
import sys
import csv
import time
import re
import argparse
import imaplib
import email
import json
from datetime import datetime
from email.mime.text import MIMEText
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# ── Config ──────────────────────────────────────────────────
load_dotenv()

OUTSCRAPER_API_KEY = os.getenv("OUTSCRAPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GMAIL_SENDER = os.getenv("GMAIL_SENDER", "contact@studioriad.com")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
SEARCH_QUERY = os.getenv("SEARCH_QUERY", "salle de mariage ile de france")
SEARCH_LIMIT = int(os.getenv("SEARCH_LIMIT", "10"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "prospection_log.csv")
ROADMAP_PATH = os.path.join(BASE_DIR, "roadmap.json")

EMAIL_SUBJECT = "Collaboration Photo/Vidéo"

DEFAULT_PROMPT_TEMPLATE = """Tu es un assistant qui rédige des emails de prospection professionnels en français.

Rédige un email court et professionnel selon cette structure :

Contenu du message :
- Accroche simple : tu as trouvé leur établissement "{nom_etablissement}" lors de recherches sur Google et tu te permets de les contacter.
- Présentation rapide : photographe et vidéaste professionnel spécialisé dans les mariages et événements.
- Proposition claire : réaliser un shooting photo/vidéo gratuit dans leur établissement pour produire du contenu qualitatif qu'ils pourront utiliser pour leur communication.
- Contrepartie : être intégré à leur carnet de prestataires recommandés pour leurs mariages et événements.
- Clôture courte : proposer un échange rapide si intéressé.

Signature :
B. Riad
www.studioriad.com
06 15 69 28 39

IMPORTANT :
- Écris UNIQUEMENT le corps de l'email, sans ligne d'objet.
- Le ton doit être chaleureux mais professionnel.
- Maximum 150 mots.
- Personnalise avec le nom de l'établissement : {nom_etablissement}
"""


# ── 1. SCRAPING GOOGLE MAPS ────────────────────────────────
def scrape_google_maps(query, limit, log=print):
    """Scrape Google Maps via Outscraper."""
    log(f"\n🔍 Recherche Google Maps : \"{query}\" (limit: {limit})")
    url = "https://api.app.outscraper.com/maps/search-v2"
    params = {"query": query, "limit": str(limit), "async": "false"}
    headers = {"X-API-KEY": OUTSCRAPER_API_KEY}
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("data", [[]])[0] if isinstance(data.get("data"), list) else []
        log(f"   ✅ {len(results)} établissements trouvés")
        return results
    except Exception as e:
        log(f"   ❌ Erreur scraping : {e}")
        return []


# ── 2. EXTRACTION EMAILS (natif → fallback Outscraper) ─────

_EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

_IGNORED_DOMAINS = {
    "sentry.io", "example.com", "wixpress.com", "prestashop.com",
    "wordpress.com", "shopify.com", "squarespace.com", "googletagmanager.com",
    "schema.org", "w3.org", "jquery.com", "unpkg.com",
}

_CONTACT_SLUGS = [
    "/contact", "/contact-us", "/nous-contacter", "/contactez-nous",
    "/about", "/a-propos", "/qui-sommes-nous", "/info",
]


def _is_valid_email(em):
    if not em or len(em) > 80:
        return False
    domain = em.split("@")[-1].lower()
    if domain in _IGNORED_DOMAINS:
        return False
    local = em.split("@")[0]
    if len(local) < 3:
        return False
    return True


def _decode_cloudflare_email(encoded):
    try:
        r = int(encoded[:2], 16)
        return "".join(chr(int(encoded[i:i+2], 16) ^ r) for i in range(2, len(encoded), 2))
    except Exception:
        return None


def _scrape_emails_from_html(html):
    soup = BeautifulSoup(html, "lxml")
    # Technique 1 : mailto
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        if href.startswith("mailto:"):
            em = href.replace("mailto:", "").split("?")[0].strip()
            if _is_valid_email(em):
                return em
    # Technique 2 : Cloudflare protection
    for tag in soup.find_all(attrs={"data-cfemail": True}):
        em = _decode_cloudflare_email(tag["data-cfemail"])
        if em and _is_valid_email(em):
            return em
    # Technique 3 : entités HTML obfusquées
    raw = html.replace("&#64;", "@").replace("&amp;#64;", "@")
    raw = raw.replace("[at]", "@").replace("[point]", ".").replace("[dot]", ".")
    for em in _EMAIL_RE.findall(raw):
        if _is_valid_email(em):
            return em
    # Technique 4 : regex texte brut
    for em in _EMAIL_RE.findall(soup.get_text(separator=" ")):
        if _is_valid_email(em):
            return em
    return None


def _native_email_scrape(website):
    headers = {"User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )}
    base = website.rstrip("/")
    if not urlparse(base).scheme:
        base = "https://" + base
    for page_url in [base] + [base + s for s in _CONTACT_SLUGS]:
        try:
            resp = requests.get(page_url, headers=headers, timeout=10, allow_redirects=True)
            if resp.status_code == 200 and "text/html" in resp.headers.get("Content-Type", ""):
                em = _scrape_emails_from_html(resp.text)
                if em:
                    return em
        except Exception:
            pass
    return None


def _outscraper_email(website):
    url = "https://api.app.outscraper.com/emails-and-contacts"
    params = {"query": website, "async": "false"}
    headers = {"X-API-KEY": OUTSCRAPER_API_KEY}
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        emails_list = data.get("data", [{}])[0].get("emails", [])
        if emails_list:
            return emails_list[0].get("value")
    except Exception as e:
        pass
    return None


def extract_email(website, log=print):
    """Scraping natif d'abord (gratuit), Outscraper en fallback."""
    if not website:
        return None, "no_website"
    em = _native_email_scrape(website)
    if em:
        return em, "native"
    em = _outscraper_email(website)
    if em:
        return em, "outscraper"
    return None, "not_found"


# ── 3. FILTRAGE & DÉDOUBLONNAGE ─────────────────────────────
def load_contacted_emails():
    contacted = set()
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("email"):
                    contacted.add(row["email"].lower())
    return contacted


def filter_prospects(prospects_with_emails, contacted):
    seen = set()
    filtered = []
    for prospect in prospects_with_emails:
        em = prospect.get("email", "")
        if not em:
            continue
        el = em.lower()
        if "studioriad" in el or el in contacted or el in seen:
            continue
        seen.add(el)
        filtered.append(prospect)
    return filtered


# ── 4. GÉNÉRATION EMAIL VIA OPENAI ──────────────────────────
def generate_email_body(prospect_name, prompt_template, log=print):
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = prompt_template.format(nom_etablissement=prospect_name)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        log(f"\n      ❌ Erreur OpenAI : {e}")
        return None


# ── 5. GMAIL VIA IMAP ───────────────────────────────────────
def create_draft_imap(to_email, subject, body):
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = GMAIL_SENDER
    msg["To"] = to_email
    msg["Subject"] = subject
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(GMAIL_SENDER, GMAIL_APP_PASSWORD)
    imap.append("[Gmail]/Brouillons", "", imaplib.Time2Internaldate(time.time()), msg.as_bytes())
    imap.logout()


# ── 6. LOGGING CSV ──────────────────────────────────────────
def log_to_csv(em, name, day="?", geo_zone="", status="draft_created"):
    file_exists = os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["email", "name", "day", "geo_zone", "date", "status"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "email": em, "name": name, "day": day,
            "geo_zone": geo_zone, "date": datetime.now().isoformat(), "status": status,
        })


# ── 7. RUN_DAY — API pour Flask ─────────────────────────────
def run_day(day: str, count: int = 10, geo_zone: str = "ile de france", log_cb=None) -> dict:
    """
    Lance la prospection pour un jour donné.
    Retourne {"success": int, "failed": int, "contacts": [...]}
    """
    log = log_cb or print

    # Charger roadmap
    if not os.path.exists(ROADMAP_PATH):
        log(f"❌ roadmap.json introuvable")
        return {"success": 0, "failed": 0, "contacts": []}

    with open(ROADMAP_PATH, "r", encoding="utf-8") as f:
        roadmap = json.load(f)

    if day not in roadmap:
        log(f"❌ Jour {day} non trouvé dans la roadmap")
        return {"success": 0, "failed": 0, "contacts": []}

    day_config = roadmap[day]
    # Remplacer la zone géo dans la query
    query = day_config["query"]
    # Remplace les zones connues par la zone demandée
    for known_zone in ["ile de france", "paris ile de france", "paris"]:
        query = query.replace(known_zone, geo_zone)
    prompt_template = day_config["prompt"]

    log(f"📅 JOUR {day} — Zone : {geo_zone}")
    log(f"   Requête : {query}")
    log(f"   Objectif : {count} brouillon(s)")
    log("=" * 55)

    # ── FIX COÛT : charger les contacts déjà traités EN PREMIER ──
    contacted = load_contacted_emails()
    log(f"   📋 {len(contacted)} contacts déjà dans le log (skip automatique)")

    # Étape 1 : Scraping Maps
    places = scrape_google_maps(query, count + 8, log)
    if not places:
        log("❌ Aucun résultat Maps. Abandon.")
        return {"success": 0, "failed": 0, "contacts": []}

    # Étape 2 : Extraction emails (natif prioritaire)
    log(f"\n📧 Extraction des emails...")
    prospects = []
    for i, place in enumerate(places):
        name = place.get("name", "Inconnu")
        website = place.get("website", "")
        log(f"   [{i+1}/{len(places)}] {name}", )

        if not website:
            log(" — pas de site web ⏭️")
            continue

        # ── FIX : skip AVANT d'appeler extract_email si déjà dans le log ──
        # On ne peut pas savoir l'email sans le chercher, mais on évite l'outscraper
        # en vérifiant d'abord avec le scraping natif rapide
        em, source = extract_email(website, log)
        if em:
            el = em.lower()
            if el in contacted:
                log(f" — {em} ⏭️ (déjà contacté, skip)")
                continue
            if "studioriad" in el:
                log(f" — propre email ⏭️")
                continue
            prospects.append({"name": name, "email": em, "website": website, "source": source})
            src_icon = "🆓" if source == "native" else "💳"
            log(f" — {em} ✅ {src_icon}")
        else:
            log(" — pas d'email trouvé ⏭️")
        time.sleep(0.5)

    # Étape 3 : Dédoublonnage final
    log(f"\n🧹 Dédoublonnage final...")
    filtered = filter_prospects(prospects, contacted)
    log(f"   {len(filtered)} prospects qualifiés (sur {len(prospects)} trouvés)")
    filtered = filtered[:count]

    if not filtered:
        log("⚠️ Aucun nouveau prospect qualifié.")
        return {"success": 0, "failed": 0, "contacts": []}

    # Étape 4 : Test IMAP
    log(f"\n🔐 Test connexion Gmail IMAP...")
    try:
        test_imap = imaplib.IMAP4_SSL("imap.gmail.com")
        test_imap.login(GMAIL_SENDER, GMAIL_APP_PASSWORD)
        test_imap.logout()
        log("   ✅ Connexion OK")
    except Exception as e:
        log(f"   ❌ Erreur IMAP : {e}")
        return {"success": 0, "failed": 0, "contacts": []}

    # Étape 5 : Génération + brouillons
    log(f"\n✨ Génération des emails...")
    success_count = 0
    failed_count = 0
    contacts_created = []

    for i, prospect in enumerate(filtered):
        name = prospect["name"]
        em = prospect["email"]
        log(f"\n   [{i+1}/{len(filtered)}] {name} ({em})")

        log(f"      🤖 OpenAI...")
        body = generate_email_body(name, prompt_template, log)
        if not body:
            log_to_csv(em, name, day, geo_zone, "openai_error")
            failed_count += 1
            continue

        log(f"      📝 Création brouillon Gmail...")
        try:
            subject = f"{EMAIL_SUBJECT} – {name}"
            create_draft_imap(em, subject, body)
            log_to_csv(em, name, day, geo_zone, "draft_created")
            success_count += 1
            contacts_created.append({"name": name, "email": em, "status": "draft_created"})
            log(f"      ✅")
        except Exception as e:
            log(f"      ❌ {e}")
            log_to_csv(em, name, day, geo_zone, f"gmail_error")
            failed_count += 1

        time.sleep(1.5)

    log(f"\n{'='*55}")
    log(f"🏁 TERMINÉ — ✅ {success_count} brouillons créés, ❌ {failed_count} échecs")
    log(f"{'='*55}")

    return {"success": success_count, "failed": failed_count, "contacts": contacts_created}


# ── 8. MAIN CLI ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Prospection automatique Studio Riad")
    parser.add_argument("--test", action="store_true", help="Mode test : 1 seul brouillon")
    parser.add_argument("--count", type=int, default=10, help="Nombre de brouillons")
    parser.add_argument("--day", type=str, default=None, help="Jour de la roadmap (1-30)")
    parser.add_argument("--geo", type=str, default="ile de france", help="Zone géographique")
    args = parser.parse_args()

    if not args.day:
        print("❌ Utilise --day X (ex: python3 prospection.py --day 3)")
        sys.exit(1)

    count = 1 if args.test else args.count
    run_day(args.day, count=count, geo_zone=args.geo)


if __name__ == "__main__":
    main()
