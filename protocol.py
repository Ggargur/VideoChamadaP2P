import socket
from enum import Enum

class ProtocolCodes():
    OK = 0x00
    NOT_OK = 0xFF
    REGISTER_NAME = 0x10
    UNREGISTER_NAME = 0x1F
    REQUEST_ADDRESS = 0x20
    NOT_FOUND = 0x2F
    FOUND = 0x2A

SERVER_PORT = 3337
# def exec(func):
#     def inner(*args, **kwargs):
#         try:
#             func(*args, **kwargs)
#         except ConnectionResetError as error:
#             print(error)
#     return inner

def send_string(connection: socket.socket, message: str) -> int:
    send_int(connection, len(message))
    return connection.send(bytes(message, encoding='utf-8'))

def recv_string(connection: socket.socket) -> str:
    size = recv_int(connection)
    return connection.recv(size).decode('utf-8')

def send_int(connection: socket.socket, value: int, length=4) -> int:
    return connection.send(int.to_bytes(value, length=length, byteorder='little',signed=False))

def recv_int(connection: socket.socket, length=4) -> int:
    return int.from_bytes(bytes=connection.recv(length), byteorder='little',signed=False)

def send_code(connection: socket.socket, value: int) -> int:
    return send_int(connection, value, length=1)

def recv_code(connection: socket.socket) -> int:
    return recv_int(connection, 1)

def serialize_address(host: str) -> int:
    if host == 'localhost':
        host = '127.0.0.1'
    l = map(int, host.split('.'))
    value = 0
    for i in range(3, -1, -1):
        value |= next(l) << (i*8)
    return value

def desserialize_address(value: int) -> str:
    return f"{(value & 0xFF_00_00_00) >> 24}.{(value & 0x00_FF_00_00) >> 16}.{(value & 0x00_00_FF_00) >> 8}.{(value & 0x00_00_00_FF)}"