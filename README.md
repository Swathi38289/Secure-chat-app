# 🛡️ Secure-Chat-App: End-to-End Encrypted Messenger

A robust, real-time chat application built with **Python**, **Flask-SocketIO**, and **AES/RSA Hybrid Encryption**. This project demonstrates a "Zero-Knowledge" architecture where the server facilitates communication but cannot read the message content.
![ScreenRecording2026-03-26114153-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/04a93c72-bfb3-405f-b342-5dfce38439f3)

---

## 📺 Live Demo & Security Audit

> **Security Proof:** At the end of the video, a database audit reveals that all messages are stored as 256-character hexadecimal strings, satisfying the **Confidentiality** pillar of the CIA Triad.

---

## 🚀 Key Features
* **Hybrid Encryption:** Uses **RSA-2048** for secure key exchange and **AES-128 (Fernet)** for high-speed message encryption.
* **Identity Persistence:** Automatically generates and manages local `.pem` keys for user identity.
* **Real-time Communication:** Built on WebSockets (SocketIO) for instantaneous duplex messaging.
* **Secure Logging:** SQLite3 backend that stores only encrypted ciphertext.
* **Standalone Executable:** Packaged as a portable `.exe` for Windows.

---

## 🛠️ Tech Stack
* **Language:** Python 3.13
* **Security:** `cryptography` library (Hazmat layer)
* **Backend:** Flask, Flask-SocketIO
* **Frontend:** Tkinter (GUI)
* **Database:** SQLite3

---

## 📂 Project Structure
```text
SECURE-CHAT-APP/
├── client/
│   ├── gui_client.py     # Main GUI Application
│   ├── encryption.py     # Cryptographic Engine (RSA/AES)
│   └── keys/             # Local storage for RSA PEM files
├── server/
│   ├── app.py            # Flask-SocketIO Server
│   ├── database.py       # Encrypted SQLite handler
│   └── data/             # Persistent encrypted logs
├── check_db.py           # Security Audit Tool
└── demo.mp4              # Technical Demonstration Video
