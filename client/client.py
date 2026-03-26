import socketio
import time
import os
import threading
from encryption import *

# Create socket client
sio = socketio.Client()

# Path Logic: Ensures it works even as a compiled .exe
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_DIR = os.path.join(BASE_DIR, "keys")
PRIV_PATH = os.path.join(KEY_DIR, "private_key.pem")

def get_identity():
    """Manages RSA Key persistence in the /keys folder."""
    if not os.path.exists(KEY_DIR):
        os.makedirs(KEY_DIR)
    
    if os.path.exists(PRIV_PATH):
        print("📂 Identity found. Loading RSA keys...")
        with open(PRIV_PATH, "rb") as f:
            # We use the cryptography library loaded via encryption.py
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        return private_key, private_key.public_key()
    else:
        print("✨ No identity found. Generating new RSA keys...")
        priv, pub = generate_rsa_keys()
        # Save the private key locally for next time
        with open(PRIV_PATH, "wb") as f:
            f.write(serialize_private_key(priv))
        return priv, pub

# Global variables
private_key, public_key = get_identity()
pub_pem = serialize_public_key(public_key)
username = ""
user_keys = {}

# =========================
# SOCKET EVENTS
# =========================

@sio.event
def connect():
    print(f"✅ Connected to Secure Server as {username}")
    sio.emit('register', {'username': username, 'public_key': pub_pem.decode()})

@sio.on('register')
def sync_keys(data):
    """Stores public keys of other online users."""
    user_keys[data['username']] = data['public_key']

@sio.on('chat_history')
def show_history(data):
    """Decrypts and displays past logs sent by the server."""
    print("\n📜 --- SECURE CHAT HISTORY ---")
    for m in data['history']:
        sender, receiver, msg_hex, key_hex, ts = m
        if receiver == username:
            try:
                # Decrypting the AES key with our RSA Private Key
                k = decrypt_key(bytes.fromhex(key_hex), private_key)
                # Decrypting the message with the AES key
                text = decrypt_message(bytes.fromhex(msg_hex), k)
                print(f"[{ts}] {sender}: {text}")
            except Exception:
                print(f"[{ts}] {sender}: (Decryption failed - possibly old key)")
        else:
            print(f"[{ts}] Me -> {receiver}: [Encrypted Message Sent]")
    print("-------------------------------\n")

@sio.on('receive_message')
def on_msg(data):
    """Handles real-time incoming messages."""
    try:
        k = decrypt_key(bytes.fromhex(data['key']), private_key)
        text = decrypt_message(bytes.fromhex(data['message']), k)
        print(f"\n🔐 {data['from']}: {text}\n👉 To: ", end="", flush=True)
    except Exception as e:
        print(f"\n❌ Secure Relay Error: {e}")

@sio.event
def disconnect():
    print("\n❌ Disconnected from server.")

# =========================
# OPERATIONAL LOGIC
# =========================

def run_chat():
    """Main input loop."""
    while True:
        try:
            to = input("👉 To (Username): ").strip()
            if not to: continue
            
            if to not in user_keys:
                print(f"⚠️ {to} is not online or hasn't shared a key yet.")
                continue

            msg = input("💬 Message: ").strip()
            if not msg: continue
            
            # Hybrid Encryption Process
            aes_k, enc_m = encrypt_message(msg)
            # Fetch recipient's public key
            recipient_pub = load_public_key(user_keys[to].encode())
            # Encrypt the AES key for the recipient
            enc_k = encrypt_key(aes_k, recipient_pub)

            sio.emit('send_message', {
                'from': username, 
                'to': to, 
                'message': enc_m.hex(), 
                'key': enc_k.hex()
            })
        except KeyboardInterrupt:
            print("\n👋 Closing app...")
            sio.disconnect()
            break

if __name__ == "__main__":
    username = input("👤 Enter your username to start: ").strip()
    if username:
        try:
            # Connect to server
            sio.connect('http://localhost:5000')
            # Run the chat loop
            run_chat()
        except Exception as e:
            print(f"❌ Could not connect to server: {e}")