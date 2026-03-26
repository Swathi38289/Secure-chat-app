import sqlite3
import os

# Look into the server/data folder from the root
DB = os.path.join("server", "data", "chat_logs.db")

if os.path.exists(DB):
    conn = sqlite3.connect(DB)
    print("\n--- 🛡️ ENCRYPTED DATABASE LOGS ---")
    for r in conn.execute("SELECT sender, receiver, encrypted_message FROM messages"):
        print(f"{r[0]} -> {r[1]} | Cipher: {r[2][:40]}...")
    conn.close()
else:
    print("❌ No database found. Send a message first!")