import socket
from enum import Enum


# Representam os diversos tipos de mensagens que podem ser passadas do cliente para o servidor e vice-versa.
class ProtocolCodes:
    OK = 0x00
    NOT_OK = 0xFF
    REGISTER_NAME = 0x10
    UNREGISTER_NAME = 0x1F
    REQUEST_ADDRESS = 0x20
    GET_ALL_REGISTERED_NAMES = 0x30
    NOT_FOUND = 0x2F
    FOUND = 0x2A
    REQUEST_CALL = 0x3F
    REFUSE_CALL = 0x3A


SERVER_PORT = 3337


# Pega mensagem em formato string assim como o socket que conecta destinatário com remetente e envia
# a mensagem para este destinatário.
def send_string(connection: socket.socket, message: str) -> int:
    send_int(connection, len(message))
    return connection.send(bytes(message, encoding="utf-8"))


# Recebe uma conexão e espera o recebimento de uma mensagem em texto do tipo string.
def recv_string(connection: socket.socket) -> str:
    size = recv_int(connection)
    return connection.recv(size).decode("utf-8")


# Pega um valor do tipo inteiro assim como o socket que conecta destinatário com remetente e envia
# esse valor para o destinatário.
def send_int(connection: socket.socket, value: int, length=4) -> int:
    return connection.send(
        int.to_bytes(value, length=length, byteorder="little", signed=False)
    )


# Recebe uma conexão e espera o recebimento de um valor do tipo inteiro.
def recv_int(connection: socket.socket, length=4) -> int:
    return int.from_bytes(
        bytes=connection.recv(length), byteorder="little", signed=False
    )


# Pega um código do protocolo assim como o socket que conecta destinatário com remetente e envia
# essa mesnsagem para o destinatário.
def send_code(connection: socket.socket, value: int) -> int:
    return send_int(connection, value, length=1)


# Recebe uma conexão e espera o recebimento de um código do protocolo.
def recv_code(connection: socket.socket) -> int:
    return recv_int(connection, 1)


# Transforma o string que representa o IP em uma int para facilitar o transporte atráves da API.
def serialize_address(host: str) -> int:
    if host == "localhost":
        host = "127.0.0.1"
    l = map(int, host.split("."))
    value = 0
    for i in range(3, -1, -1):
        value |= next(l) << (i * 8)
    return value


# Pega o endereço de ip, recebido recebido em int e retransforma em uma string que pode ser ultilizada pela API socket.
def desserialize_address(value: int) -> str:
    return f"{(value & 0xFF_00_00_00) >> 24}.{(value & 0x00_FF_00_00) >> 16}.{(value & 0x00_00_FF_00) >> 8}.{(value & 0x00_00_00_FF)}"
