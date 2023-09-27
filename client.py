from tkinter import *
from tkinter import ttk

from protocol import *

import threading
import time

import socket

user_name = ""
client_names: list[str] = []

def connect_server() -> socket.socket:
    SERVER_ADDRESS = ('localhost', SERVER_PORT)
    server_conn= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_conn.connect(SERVER_ADDRESS)
    return server_conn

def start_listening() -> socket.socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.bind(("0.0.0.0", 0))
    s.listen()
    return s

def register_name():
    global user_entry, user_name

    user_name = user_entry.get()
    user_entry.delete(0, 100)
    server_conn = connect_server()
    
    send_code(server_conn, ProtocolCodes.REGISTER_NAME)
    send_string(server_conn, user_name)
    send_int(server_conn, 2, length=2)
    
    status = recv_code(server_conn)
    
    if status == ProtocolCodes.OK:
        print("Registrador com sucesso")
    elif status == ProtocolCodes.NOT_OK:
        pass
    server_conn.close()

def request_name():
    user_name = user_entry.get()
    server_conn = connect_server()
    
    send_code(server_conn, ProtocolCodes.REQUEST_ADDRESS)
    send_string(server_conn, user_name)

    status = recv_code(server_conn)
    host = desserialize_address(recv_int(server_conn))
    port = recv_int(server_conn, 2)

    print(f"Nome {user_name} está disponível em {host}:{port}")

def on_closing():
    global window
    window.destroy()

window = Tk()

ttk.Label(window, text="Nome de usuário: ").pack(side='left')

user_entry = ttk.Entry(window)
user_entry.pack(side='left')

ttk.Button(window, text="Cadastrar", command=register_name).pack(pady=5)
ttk.Button(window, text="Requisitar", command=request_name).pack(pady=5)
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
