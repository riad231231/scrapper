import json
import os
import csv
import io
import threading
import queue
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, Response, stream_with_context

from .db import get_contacts, get_day_stats, get_setting, set_setting, save_contact, get_db

bp = Blueprint("main", __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROADMAP_PATH = os.path.join(BASE_DIR, "roadmap.json")

# ── État global du job en cours ──────────────────────────────
_job_state = {
    "running": False,
    "day": None,
    "queue": queue.Queue(),
}

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


# ── Pages ────────────────────────────────────────────────────
@bp.route("/")
def index():
    return render_template("index.html")


# ── API Roadmap ──────────────────────────────────────────────
@bp.route("/api/roadmap")
def get_roadmap():
    if not os.path.exists(ROADMAP_PATH):
        return jsonify({"error": "roadmap.json introuvable"}), 404
    with open(ROADMAP_PATH, "r", encoding="utf-8") as f:
        roadmap = json.load(f)
    day_stats = get_day_stats()
    result = []
    for day, config in roadmap.items():
        result.append({
            "day": day,
            "cible": CIBLES.get(day, "?"),
            "query": config.get("query", ""),
            "prompt": config.get("prompt", ""),
            "contacts_created": day_stats.get(day, 0),
        })
    return jsonify(result)


@bp.route("/api/roadmap/<day>", methods=["POST"])
def update_roadmap_day(day):
    data = request.json
    if not os.path.exists(ROADMAP_PATH):
        return jsonify({"error": "roadmap.json introuvable"}), 404
    with open(ROADMAP_PATH, "r", encoding="utf-8") as f:
        roadmap = json.load(f)
    if day not in roadmap:
        return jsonify({"error": "Jour non trouvé"}), 404
    if "query" in data:
        roadmap[day]["query"] = data["query"]
    if "prompt" in data:
        roadmap[day]["prompt"] = data["prompt"]
    with open(ROADMAP_PATH, "w", encoding="utf-8") as f:
        json.dump(roadmap, f, ensure_ascii=False, indent=4)
    return jsonify({"ok": True})


# ── API Settings ─────────────────────────────────────────────
@bp.route("/api/settings", methods=["GET"])
def api_get_settings():
    return jsonify({
        "geo_zone": get_setting("geo_zone", "ile de france"),
        "default_count": get_setting("default_count", "10"),
    })


@bp.route("/api/settings", methods=["POST"])
def api_save_settings():
    data = request.json
    for key in ["geo_zone", "default_count"]:
        if key in data:
            set_setting(key, data[key])
    # Si geo_zone changée, mettre à jour les queries
    if "geo_zone" in data and data.get("update_queries"):
        _apply_geo_zone_to_roadmap(data["geo_zone"])
    return jsonify({"ok": True})


def _apply_geo_zone_to_roadmap(new_zone):
    """Remplace la zone géo dans toutes les queries de la roadmap."""
    if not os.path.exists(ROADMAP_PATH):
        return
    with open(ROADMAP_PATH, "r", encoding="utf-8") as f:
        roadmap = json.load(f)
    zones_to_replace = ["ile de france", "paris ile de france", "paris", "bretagne", "lyon", "marseille", "bordeaux", "toulouse", "nantes", "lille"]
    for day_config in roadmap.values():
        q = day_config.get("query", "")
        for zone in zones_to_replace:
            if zone in q.lower():
                day_config["query"] = q.lower().replace(zone, new_zone)
                break
    with open(ROADMAP_PATH, "w", encoding="utf-8") as f:
        json.dump(roadmap, f, ensure_ascii=False, indent=4)


# ── API Run (lancement d'un jour) ────────────────────────────
@bp.route("/api/run/<day>", methods=["POST"])
def run_day_api(day):
    if _job_state["running"]:
        return jsonify({"error": "Un job est déjà en cours"}), 409

    data = request.json or {}
    count = int(data.get("count", get_setting("default_count", "10")))
    geo_zone = data.get("geo_zone", get_setting("geo_zone", "ile de france"))

    def _run():
        _job_state["running"] = True
        _job_state["day"] = day

        # Vider l'ancienne queue
        while not _job_state["queue"].empty():
            _job_state["queue"].get_nowait()

        def log_cb(msg):
            _job_state["queue"].put(str(msg))

        try:
            from prospection import run_day
            result = run_day(day, count=count, geo_zone=geo_zone, log_cb=log_cb)
            # Sauvegarder dans la DB
            for contact in result.get("contacts", []):
                save_contact(
                    email=contact["email"],
                    name=contact["name"],
                    day=day,
                    geo_zone=geo_zone,
                    status=contact["status"],
                )
        except Exception as e:
            log_cb(f"❌ Erreur : {e}")
        finally:
            _job_state["running"] = False
            _job_state["queue"].put("__DONE__")

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return jsonify({"ok": True, "day": day, "count": count, "geo_zone": geo_zone})


# ── API Stream SSE (logs temps réel) ─────────────────────────
@bp.route("/api/stream")
def stream():
    def generate():
        yield "data: connected\n\n"
        while True:
            try:
                msg = _job_state["queue"].get(timeout=30)
                if msg == "__DONE__":
                    yield "data: __DONE__\n\n"
                    break
                # Échapper les newlines pour SSE
                safe = str(msg).replace("\n", " ").replace("\r", "")
                yield f"data: {safe}\n\n"
            except queue.Empty:
                yield "data: __PING__\n\n"
    return Response(stream_with_context(generate()), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


# ── API Status ───────────────────────────────────────────────
@bp.route("/api/status")
def status():
    return jsonify({
        "running": _job_state["running"],
        "day": _job_state["day"],
    })


# ── API Contacts ─────────────────────────────────────────────
@bp.route("/api/contacts")
def api_contacts():
    day = request.args.get("day")
    status = request.args.get("status")
    contacts = get_contacts(day=day, status=status)
    return jsonify(contacts)


@bp.route("/api/contacts/export")
def export_contacts():
    contacts = get_contacts()
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["email", "name", "day", "geo_zone", "date", "status", "source"])
    writer.writeheader()
    for c in contacts:
        writer.writerow({k: c.get(k, "") for k in ["email", "name", "day", "geo_zone", "date", "status", "source"]})
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=contacts_{datetime.now().strftime('%Y%m%d')}.csv"}
    )


# ── API Stats ────────────────────────────────────────────────
@bp.route("/api/stats")
def api_stats():
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM contacts WHERE status='draft_created'").fetchone()[0]
    today = conn.execute(
        "SELECT COUNT(*) FROM contacts WHERE status='draft_created' AND date LIKE ?",
        (datetime.now().strftime("%Y-%m-%d") + "%",)
    ).fetchone()[0]
    conn.close()
    day_stats = get_day_stats()
    days_done = len([d for d, c in day_stats.items() if c > 0])
    return jsonify({
        "total_contacts": total,
        "today": today,
        "days_done": days_done,
        "days_total": 30,
    })
