import socket
import threading
import sys

from log import *

from protocol import *

HOST = "localhost"
PORT = SERVER_PORT

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# clients: dict[str, tuple[socket.socket, socket.AddressInfo]] = {}

clients_name_to_address: dict[str, tuple[str, int]] = {}


# Recebe um nome por meio de mensagem pelo socket e envia as informações de IP e porta ligadas a esse nome para o cliente que os requisitou.
# Se o nome estiver cadastrado será o seu respectivo IP será transformado de string para int e será enviado junto com a porta,
# caso contrário será enviada uma mensagem de erro para o cliente.
def handle_request_address(conn: socket.socket):
    global clients_name_to_address

    requested_name = recv_string(conn)

    if not requested_name in clients_name_to_address:
        log(f"requested_address: {requested_name} não encontrado")
        send_code(conn, ProtocolCodes.NOT_FOUND)
        return

    send_code(conn, ProtocolCodes.FOUND)
    log(f"requested_address: {requested_name} encontrado")
    send_int(conn, serialize_address(clients_name_to_address[requested_name][0]))
    send_int(conn, clients_name_to_address[requested_name][1])


# Descadastra um nome recebido por uma mensagem na socket e o retira no dicionário de nomes.
# Se este nome não estiver previamente cadastrado, servidor retornará uma mensagem de erro ao cliente,
# caso contrário enviará uma mensagem de sucesso.
def handle_unregister_name(conn: socket.socket):
    name = recv_string(conn)
    if not name in clients_name_to_address:
        send_code(conn, ProtocolCodes.NOT_OK)
        print(f"Nome: {name} não registrado")
        return
    clients_name_to_address.pop(name)
    send_code(conn, ProtocolCodes.OK)
    print(f"Nome: {name} descadastrado")


# Cadastra um nome recebido por uma mensagem na socket e o registra no dicionário de nomes, junto com seu endereço e porta.
# Se este nome já estiver previamente cadastrado, servidor retornará uma mensagem de erro ao cliente,
#  caso contrário enviará uma mensagem de sucesso.
def handle_register_name(conn: socket.socket):
    global clients_name_to_address

    name = recv_string(conn)
    host = conn.getpeername()[0]
    port = recv_int(conn, 2)
    if name in clients_name_to_address:
        log(f"register_name: {name} já em uso")
        send_code(conn, ProtocolCodes.NOT_OK)
        return

    clients_name_to_address[name] = (host, port)
    log(f"register_name: {name} registrado")
    send_code(conn, ProtocolCodes.OK)


# Reconhece uma informação recebida por uma conexão, tratando indicar o método correto para o tipo de mensagem recebida e termina encerrando a conexão.
# Essas podendo ser: cadastramento ou descadastramento diferentes clientes ou requisições.
def handle_connection(conn: socket.socket, address: socket.AddressInfo):
    code = recv_code(conn)
    if code == ProtocolCodes.REGISTER_NAME:
        handle_register_name(conn)
    elif code == ProtocolCodes.REQUEST_ADDRESS:
        handle_request_address(conn)
    elif code == ProtocolCodes.UNREGISTER_NAME:
        handle_unregister_name(conn)
    conn.close()
    print(f"Conexão de {address} encerrada")


# Abre a porta do servidor e começa a escutar por mensagens recebidas atráves dessa porta.
# A função fuja responsável por tratar as meensagens recebidas pela porta é colocada em uma thread, assim paralelizando o processo.
def main():
    server.bind((HOST, PORT))
    server.listen()

    log(f"Servidor escutando em {HOST}:{PORT}")

    while True:
        conn_tuple = server.accept()
        log(f"Conexão de {conn_tuple[1]}", 1)
        t = threading.Thread(target=handle_connection, args=conn_tuple, daemon=True)
        t.start()


main()
server.close()
