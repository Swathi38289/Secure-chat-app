import tkinter as tk
from tkinter import scrolledtext, messagebox
import socketio
import os
from encryption import *
class SecureChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Swathi's Secure Messenger")
        
        # Path Logic for keys
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.key_dir = os.path.join(self.base_dir, "keys")
        self.priv_path = os.path.join(self.key_dir, "private_key.pem")
        
        # Identity
        self.private_key, self.public_key = self.get_id()
        self.username = ""
        self.user_keys = {}
        
        self.setup_ui()
        self.sio = socketio.Client()
        self.setup_socket()

    def get_id(self):
        os.makedirs(self.key_dir, exist_ok=True)
        if os.path.exists(self.priv_path):
            with open(self.priv_path, "rb") as f:
                priv = serialization.load_pem_private_key(f.read(), password=None)
            return priv, priv.public_key()
        else:
            priv, pub = generate_rsa_keys()
            with open(self.priv_path, "wb") as f:
                f.write(serialize_private_key(priv))
            return priv, pub

    def setup_ui(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=10)
        tk.Label(self.login_frame, text="Username:").pack(side=tk.LEFT)
        self.u_ent = tk.Entry(self.login_frame)
        self.u_ent.pack(side=tk.LEFT)
        tk.Button(self.login_frame, text="Connect", command=self.connect_server).pack(side=tk.LEFT)

        self.chat_box = scrolledtext.ScrolledText(self.root, state='disabled', width=50, height=15)
        self.chat_box.pack(padx=10, pady=10)

        self.msg_frame = tk.Frame(self.root)
        self.msg_frame.pack(pady=5)
        tk.Label(self.msg_frame, text="To:").pack(side=tk.LEFT)
        self.to_ent = tk.Entry(self.msg_frame, width=10)
        self.to_ent.pack(side=tk.LEFT)
        self.m_ent = tk.Entry(self.msg_frame, width=25)
        self.m_ent.pack(side=tk.LEFT)
        tk.Button(self.msg_frame, text="Send", command=self.send_msg).pack(side=tk.LEFT)

    def setup_socket(self):
        @self.sio.on('register')
        def on_reg(data): self.user_keys[data['username']] = data['public_key']
        
        @self.sio.on('receive_message')
        def on_msg(data):
            try:
                k = decrypt_key(bytes.fromhex(data['key']), self.private_key)
                txt = decrypt_message(bytes.fromhex(data['message']), k)
                self.update_chat(f"{data['from']}: {txt}")
            except: pass

    def connect_server(self):
        self.username = self.u_ent.get().strip()
        if self.username:
            try:
                self.sio.connect('http://localhost:5000')
                pub_pem = serialize_public_key(self.public_key)
                self.sio.emit('register', {'username': self.username, 'public_key': pub_pem.decode()})
                self.u_ent.config(state='disabled')
                messagebox.showinfo("Logged In", f"Welcome {self.username}")
            except: messagebox.showerror("Error", "Server Offline")

    def send_msg(self):
        to, msg = self.to_ent.get().strip(), self.m_ent.get().strip()
        if to in self.user_keys and msg:
            aes_k, enc_m = encrypt_message(msg)
            enc_k = encrypt_key(aes_k, load_public_key(self.user_keys[to].encode()))
            self.sio.emit('send_message', {'from': self.username, 'to': to, 'message': enc_m.hex(), 'key': enc_k.hex()})
            self.update_chat(f"Me -> {to}: {msg}")
            self.m_ent.delete(0, tk.END)

    def update_chat(self, text):
        self.chat_box.config(state='normal')
        self.chat_box.insert(tk.END, text + "\n")
        self.chat_box.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureChatApp(root)
    root.mainloop()