#!/usr/bin/env python3
"""
=============================================================
  BATCH PROSPECTION — Studio Riad
  Lance automatiquement les jours 3 à 30 de la roadmap
  avec pause configurable entre chaque session.
=============================================================
Usage:
  python3 scripts/run_batch.py                # Jours 3 à 30
  python3 scripts/run_batch.py --start 5     # Reprend au jour 5
  python3 scripts/run_batch.py --end 10      # S'arrête au jour 10
  python3 scripts/run_batch.py --count 5     # 5 prospects par jour
  python3 scripts/run_batch.py --pause 60    # 60s de pause entre jours
  python3 scripts/run_batch.py --test        # Test mode (1 seul brouillon/jour)
  python3 scripts/run_batch.py --dry         # Affiche le plan sans exécuter
=============================================================
"""

import os
import sys
import time
import argparse
import subprocess
import json
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROADMAP_PATH = os.path.join(BASE_DIR, "roadmap.json")
SCRIPT_PATH = os.path.join(BASE_DIR, "prospection.py")
BATCH_LOG_PATH = os.path.join(BASE_DIR, "batch_log.json")

# Couleurs terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

CIBLES = {
    "1": "Domaines mariage (1)", "2": "Domaines mariage (2)",
    "3": "Traiteurs prestige (1)", "4": "Traiteurs prestige (2)",
    "5": "Negafa / mises en beauté (1)", "6": "Negafa / mises en beauté (2)",
    "7": "Wedding Planners (1)", "8": "Wedding Planners (2)",
    "9": "Fleuristes mariage (1)", "10": "Fleuristes mariage (2)",
    "11": "DJ / Animateurs (1)", "12": "DJ / Animateurs (2)",
    "13": "Boutiques robes (1)", "14": "Boutiques robes (2)",
    "15": "Cake Designers (1)", "16": "Cake Designers (2)",
    "17": "Makeup Artists (1)", "18": "Makeup Artists (2)",
    "19": "Location voitures luxe (1)", "20": "Location voitures luxe (2)",
    "21": "Orchestres mariage (1)", "22": "Orchestres mariage (2)",
    "23": "Bijouteries / Joaillers (1)", "24": "Bijouteries / Joaillers (2)",
    "25": "Photobooth / Box photos (1)", "26": "Photobooth / Box photos (2)",
    "27": "Location matériel réception (1)", "28": "Location matériel réception (2)",
    "29": "Créateurs faire-parts (1)", "30": "Créateurs faire-parts (2)",
}


def load_batch_log():
    """Charge le log du batch (pour reprise)."""
    if os.path.exists(BATCH_LOG_PATH):
        with open(BATCH_LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"completed": [], "failed": [], "started_at": None, "last_run": None}


def save_batch_log(log):
    """Sauvegarde le log du batch."""
    log["last_run"] = datetime.now().isoformat()
    with open(BATCH_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)


def format_duration(seconds):
    """Formate une durée en mm:ss."""
    return str(timedelta(seconds=int(seconds))).lstrip("0:") or "0s"


def display_plan(days, count, pause_s, test_mode):
    """Affiche le plan d'exécution."""
    print(f"\n{BOLD}{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}  📋 PLAN BATCH — Studio Riad{RESET}")
    print(f"{BOLD}{CYAN}{'='*60}{RESET}")
    print(f"  🗓️  Jours planifiés : {days[0]} → {days[-1]} ({len(days)} jours)")
    print(f"  📧  Prospects/jour  : {'1 (TEST)' if test_mode else count}")
    print(f"  ⏱️   Pause entre    : {pause_s}s")
    est_total = len(days) * (count * 45 + pause_s)  # ~45s/prospect
    print(f"  🕐  Durée estimée  : ~{format_duration(est_total)}")
    print(f"\n  {'Jour':<8} {'Cible':<35} {'Statut'}")
    print(f"  {'-'*8} {'-'*35} {'-'*10}")
    for d in days:
        cible = CIBLES.get(str(d), "?")
        print(f"  Jour {d:<3} {cible:<35} ⏳ planifié")
    print(f"{BOLD}{CYAN}{'='*60}{RESET}\n")


def run_day(day, count, test_mode):
    """Lance prospection.py pour un jour donné."""
    cmd = [sys.executable, SCRIPT_PATH, "--day", str(day)]
    if test_mode:
        cmd.append("--test")
    else:
        cmd.extend(["--count", str(count)])

    result = subprocess.run(cmd, capture_output=False, text=True)
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Batch prospection Studio Riad")
    parser.add_argument("--start", type=int, default=3, help="Jour de départ (défaut: 3)")
    parser.add_argument("--end", type=int, default=30, help="Jour de fin (défaut: 30)")
    parser.add_argument("--count", type=int, default=10, help="Prospects par jour (défaut: 10)")
    parser.add_argument("--pause", type=int, default=30, help="Pause en secondes entre jours (défaut: 30)")
    parser.add_argument("--test", action="store_true", help="Mode test (1 brouillon/jour)")
    parser.add_argument("--dry", action="store_true", help="Affiche le plan sans exécuter")
    parser.add_argument("--resume", action="store_true", help="Reprend en sautant les jours déjà complétés")
    args = parser.parse_args()

    # Vérification roadmap
    if not os.path.exists(ROADMAP_PATH):
        print(f"{RED}❌ roadmap.json introuvable dans {BASE_DIR}{RESET}")
        sys.exit(1)

    with open(ROADMAP_PATH, "r", encoding="utf-8") as f:
        roadmap = json.load(f)

    # Jours disponibles dans la range
    days = [d for d in range(args.start, args.end + 1) if str(d) in roadmap]

    if not days:
        print(f"{RED}❌ Aucun jour valide entre {args.start} et {args.end}{RESET}")
        sys.exit(1)

    # Reprise (skip des jours déjà faits)
    batch_log = load_batch_log()
    if args.resume and batch_log["completed"]:
        already_done = [int(d) for d in batch_log["completed"]]
        days_orig = len(days)
        days = [d for d in days if d not in already_done]
        print(f"{YELLOW}⏭️  Reprise : {days_orig - len(days)} jours déjà complétés, {len(days)} restants{RESET}")

    if not days:
        print(f"{GREEN}✅ Tous les jours sont déjà complétés !{RESET}")
        sys.exit(0)

    # Affichage du plan
    display_plan(days, args.count, args.pause, args.test)

    if args.dry:
        print(f"{YELLOW}🏜️  Mode DRY — aucun email envoyé.{RESET}\n")
        return

    # Démarrage du batch
    input(f"{BOLD}Appuie sur ENTRÉE pour démarrer le batch...{RESET} ")
    print()

    batch_log["started_at"] = batch_log["started_at"] or datetime.now().isoformat()
    start_time = time.time()
    success_days = []
    failed_days = []

    for i, day in enumerate(days):
        cible = CIBLES.get(str(day), "?")
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}{CYAN}  📅 JOUR {day}/{days[-1]} — {cible}{RESET}")
        print(f"  ⏱️  {datetime.now().strftime('%H:%M:%S')}")
        print(f"{BOLD}{'='*60}{RESET}")

        success = run_day(day, args.count, args.test)

        if success:
            success_days.append(day)
            batch_log["completed"].append(str(day))
            print(f"\n{GREEN}✅ Jour {day} terminé avec succès !{RESET}")
        else:
            failed_days.append(day)
            batch_log["failed"].append(str(day))
            print(f"\n{RED}❌ Jour {day} a échoué (vérifie les logs ci-dessus).{RESET}")

        save_batch_log(batch_log)

        # Pause entre jours (sauf le dernier)
        if i < len(days) - 1:
            remaining = len(days) - i - 1
            print(f"\n{YELLOW}  ⏸️  Pause de {args.pause}s avant le jour {days[i+1]}... ({remaining} jours restants){RESET}")
            for t in range(args.pause, 0, -1):
                print(f"\r  {t}s... ", end="", flush=True)
                time.sleep(1)
            print()

    # Résumé final
    elapsed = time.time() - start_time
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{GREEN}  🏁 BATCH TERMINÉ !{RESET}")
    print(f"  ✅ Jours réussis  : {len(success_days)}/{len(days)} ({', '.join(str(d) for d in success_days)})")
    if failed_days:
        print(f"  ❌ Jours échoués : {', '.join(str(d) for d in failed_days)}")
        print(f"     👉 Relance avec : python3 scripts/run_batch.py --start {failed_days[0]} --resume")
    print(f"  ⏱️   Durée totale  : {format_duration(elapsed)}")
    print(f"  📊 Log batch      : {BATCH_LOG_PATH}")
    print(f"  📧 Log emails     : prospection_log.csv")
    print(f"{BOLD}{'='*60}{RESET}\n")


if __name__ == "__main__":
    main()
