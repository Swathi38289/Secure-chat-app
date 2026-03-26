from flask import Flask
from flask_socketio import SocketIO
from database import init_db
from socket_handler import register_handlers

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

init_db()
register_handlers(socketio)

if __name__ == "__main__":
    print("🚀 Server active on port 5000")
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)