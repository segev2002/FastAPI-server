import sqlite3

DB_FILE = "logs_db.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            method TEXT,
            route TEXT,
            duration_ms REAL,
            create_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_log(description, method, route, duration_ms):
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT INTO logs (description, method, route, duration_ms) VALUES (?, ?, ?, ?)",
        (description, method, route, duration_ms),
    )
    conn.commit()
    conn.close()
