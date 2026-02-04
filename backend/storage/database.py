import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "chat.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id TEXT,
        role TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def save_message(conversation_id: str, role: str, message: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO messages (conversation_id, role, message) VALUES (?, ?, ?)",
        (conversation_id, role, message)
    )

    conn.commit()
    conn.close()

def get_last_messages(conversation_id: str, limit: int = 5):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT role, message FROM messages
        WHERE conversation_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (conversation_id, limit)
    )

    rows = cur.fetchall()
    conn.close()

    return rows[::-1]  # reverse to oldest → newest
