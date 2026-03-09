import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "prospection.db")
CSV_PATH = os.path.join(BASE_DIR, "prospection_log.csv")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            name TEXT,
            day TEXT DEFAULT '?',
            geo_zone TEXT DEFAULT '',
            date TEXT,
            status TEXT,
            source TEXT DEFAULT 'unknown'
        );
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        );
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT,
            geo_zone TEXT,
            count INTEGER,
            started_at TEXT,
            finished_at TEXT,
            status TEXT DEFAULT 'running',
            success INTEGER DEFAULT 0,
            failed INTEGER DEFAULT 0
        );
    """)
    conn.commit()

    # Valeurs par défaut
    defaults = {
        "geo_zone": "ile de france",
        "default_count": "10",
    }
    for key, val in defaults.items():
        conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (key, val))
    conn.commit()

    # Migration du CSV existant si la DB est vide
    _migrate_csv(conn)
    conn.close()


def _migrate_csv(conn):
    """Migre les données du CSV vers SQLite lors du premier démarrage."""
    import csv as csv_module
    if not os.path.exists(CSV_PATH):
        return
    count = conn.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
    if count > 0:
        return  # Déjà migré
    try:
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv_module.DictReader(f)
            for row in reader:
                try:
                    conn.execute(
                        "INSERT OR IGNORE INTO contacts (email, name, day, geo_zone, date, status) VALUES (?,?,?,?,?,?)",
                        (
                            row.get("email", ""),
                            row.get("name", ""),
                            row.get("day", "?"),
                            row.get("geo_zone", ""),
                            row.get("date", datetime.now().isoformat()),
                            row.get("status", "draft_created"),
                        )
                    )
                except Exception:
                    pass
        conn.commit()
        print(f"✅ Migration CSV → SQLite effectuée")
    except Exception as e:
        print(f"⚠️ Erreur migration CSV : {e}")


def get_setting(key, default=""):
    conn = get_db()
    row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else default


def set_setting(key, value):
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()


def save_contact(email, name, day="?", geo_zone="", status="draft_created", source="unknown"):
    conn = get_db()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO contacts (email, name, day, geo_zone, date, status, source) VALUES (?,?,?,?,?,?,?)",
            (email, name, day, geo_zone, datetime.now().isoformat(), status, source)
        )
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()


def get_contacts(day=None, status=None, limit=500):
    conn = get_db()
    query = "SELECT * FROM contacts WHERE 1=1"
    params = []
    if day:
        query += " AND day=?"
        params.append(day)
    if status:
        query += " AND status=?"
        params.append(status)
    query += " ORDER BY date DESC LIMIT ?"
    params.append(limit)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_day_stats():
    """Retourne le nombre de contacts créés par jour."""
    conn = get_db()
    rows = conn.execute(
        "SELECT day, COUNT(*) as count FROM contacts WHERE status='draft_created' GROUP BY day"
    ).fetchall()
    conn.close()
    return {row["day"]: row["count"] for row in rows}
