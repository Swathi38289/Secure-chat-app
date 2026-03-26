from flask_socketio import emit, join_room
from database import save_message, get_chat_history

users = {}

def register_handlers(socketio):
    @socketio.on('register')
    def handle_reg(data):
        u, k = data['username'], data['public_key']
        users[u] = k
        join_room(u)
        print(f"👤 {u} is online.")
        emit('user_list', list(users.keys()), broadcast=True)
        for name, key in users.items():
            emit('register', {'username': name, 'public_key': key}, broadcast=True)
        
        history = get_chat_history(u)
        emit('chat_history', {'history': history}, room=u)

    @socketio.on('send_message')
    def handle_msg(data):
        save_message(data['from'], data['to'], data['message'], data['key'])
        if data['to'] in users:
            emit('receive_message', data, room=data['to'])