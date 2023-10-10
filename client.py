from tkinter import *
from tkinter import ttk

from protocol import *

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

def register_name(user_name: str):
    server_conn = connect_server()
    
    send_code(server_conn, ProtocolCodes.REGISTER_NAME)
    send_string(server_conn, user_name)
    send_int(server_conn, 2, length=2)
    
    status = recv_code(server_conn)
    
    if status == ProtocolCodes.OK:
        print("Registrador com sucesso")
    elif status == ProtocolCodes.NOT_OK:
        print(f"Nome {user_name} já utilizado")
    server_conn.close()

def unregister_name(user_name: str):
    server_conn = connect_server()

    send_code(server_conn, ProtocolCodes.UNREGISTER_NAME)
    send_string(server_conn, user_name)

    status = recv_code(server_conn)

    if status == ProtocolCodes.NOT_OK:
        print(f"Nome {user_name} não registrado")
        return
    print(f"Nome {user_name} descadrastado")
    server_conn.close()

def request_name(user_name: str):
    server_conn = connect_server()
    
    send_code(server_conn, ProtocolCodes.REQUEST_ADDRESS)
    send_string(server_conn, user_name)

    status = recv_code(server_conn)
    if status == ProtocolCodes.NOT_FOUND:
        print(f"Endereço de {user_name} não encontrado")
        return
    host = desserialize_address(recv_int(server_conn))
    port = recv_int(server_conn, 2)

    print(f"Nome {user_name} está disponível em {host}:{port}")
    
