import sqlite3
import os
from datetime import datetime

# Path Logic: Look for 'data' folder inside the 'server' directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "chat_logs.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        receiver TEXT,
        encrypted_message TEXT,
        encrypted_key TEXT,
        timestamp TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_message(sender, receiver, enc_msg, enc_key):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (sender, receiver, encrypted_message, encrypted_key, timestamp) VALUES (?, ?, ?, ?, ?)",
                   (sender, receiver, enc_msg, enc_key, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_chat_history(username):
    if not os.path.exists(DB_PATH): return []
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT sender, receiver, encrypted_message, encrypted_key, timestamp FROM messages WHERE sender=? OR receiver=? ORDER BY timestamp ASC", (username, username))
    rows = cursor.fetchall()
    conn.close()
    return rows