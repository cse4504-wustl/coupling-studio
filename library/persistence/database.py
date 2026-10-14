import sqlite3

import config


def get_connection():
    return sqlite3.connect(config.DB_PATH)


def init_db(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS books (
            isbn        TEXT PRIMARY KEY,
            title       TEXT NOT NULL,
            author      TEXT NOT NULL,
            borrower_id TEXT,
            due_date    TEXT
        );
        CREATE TABLE IF NOT EXISTS members (
            id         TEXT PRIMARY KEY,
            name       TEXT NOT NULL,
            type       TEXT NOT NULL,
            balance    REAL NOT NULL,
            daily_fine REAL NOT NULL
        );
    """)
    conn.executemany(
        "INSERT OR REPLACE INTO members VALUES (?, ?, ?, ?, ?)",
        [
            ("M001", "Ada Lovelace", "student", 0.0, 0.25),
            ("M002", "Grace Hopper", "faculty", 0.0, 0.10),
        ],
    )
    conn.commit()
