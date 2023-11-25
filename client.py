from protocol import *
import socket
import vidstream
from vidstream import StreamingServer
import threading

user_name = ""
client_names: list[str] = []
accept_request_method : function

video_streamer : vidstream.CameraClient
audio_streamer : vidstream.AudioSender

audio_listener : vidstream.AudioReceiver
streaming_server : vidstream.StreamingServer

# Conecta-se ao servidor.
def connect_server() -> socket.socket:
    SERVER_ADDRESS = ("localhost", SERVER_PORT)
    server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_conn.connect(SERVER_ADDRESS)
    return server_conn


# Prepara uma porta UDP de um cliente para iniciar uma conexão com outro cliente.
def start_listening() -> socket.socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.bind(("0.0.0.0", 0))
    return s


# Envia para o servidor uma mesagem para o cadastramento de um nome.
# Apresenta mensagem de erro caso o servidor detecte um erro na transação (pelo fato do nome já estar cadastrado),
# caso contrário apresenta uma mensagem de sucesso.
def register_name(user_name: str):
    server_conn = connect_server()
    s = start_listening()
    start_listening_to_requests(s)
    (localhost, port) = s.getsockname()

    send_code(server_conn, ProtocolCodes.REGISTER_NAME)
    send_string(server_conn, user_name)
    send_int(server_conn, port, length=2)

    status = recv_code(server_conn)

    if status == ProtocolCodes.OK:
        print("Registrado com sucesso")
    elif status == ProtocolCodes.NOT_OK:
        print(f"Nome {user_name} já utilizado")
    server_conn.close()


# Envia para o servidor uma mesagem para o descadastramento de um nome.
# Apresenta mensagem de erro caso o servidor detecte um erro na transação (pelo fato do nome não estar cadastrado),
# caso contrário apresenta uma mensagem de sucesso.
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


# Envia para o servidor uma requisição por um endereço e porta, atráves de um nome.
# Apresenta mensagem de erro caso o servidor detecte um erro na transação (pelo fato do nome não estar cadastrado),
# caso contrário transforma o endereço IP em string, e apresenta o nome junto com seus respectivos endereço e porta.
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

def get_all_registered_names():
    server_conn = connect_server()

    send_code(server_conn, ProtocolCodes.GET_ALL_REGISTERED_NAMES)

    n_codes = recv_int(server_conn)

    names = []
    for i in range(n_codes):
        name = recv_string(server_conn)
        names.append(name)
    
    print("nomes: ")
    print(names)
    return names

def start_listener_server():
    global audio_listener, streaming_server
    audio_listener = vidstream.AudioReceiver("0.0.0.0", 9998)
    streaming_server = vidstream.StreamingServer('0.0.0.0', 9999)
    
    audio_listener.start_server()
    streaming_server.start_server()


def start_listing_to_stream():
    thead_audio = threading.Thread(target=start_listener_server)
    thead_audio.start()

def stop_call():
    if video_streamer is not None:
        video_streamer.stop_stream
    if audio_streamer is not None:
        audio_streamer.stop_stream()
    if audio_listener is not None:
        audio_listener.stop_server()
    if streaming_server is not None:
        streaming_server.stop_server()

def start_streaming_server():
    video_streamer = vidstream.CameraClient('0.0.0.0', 9997)
    audio_streamer = vidstream.AudioSender("0.0.0.0",9996)
    
    audio_streamer.start_stream()
    video_streamer.start_stream()

def start_listening_to_requests(socket : socket.socket):
    threading.Thread(target=lambda : listen_to_requests(socket))

def listen_to_requests(socket : socket.socket):
    code = recv_code(socket)
    if(code == ProtocolCodes.REQUEST_CALL): # Inserir input para recusar
        accepted = True
        if(accept_request_method is not None):
            accepted = accept_request_method()
        if accepted:
            start_streaming()
            start_listing_to_stream()
            send_code(ProtocolCodes.ACCEPT_CALL)
        else:
            send_code(ProtocolCodes.REFUSE_CALL)
        print("Me foi requestado uma chamada.")
    start_listening_to_requests(socket)
        


def start_streaming():
    streamer = threading.Thread(target=start_streaming_server)
    streamer.start()

def connect_with(address : str, port : int):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((address, port))
    start_listing_to_stream()
    send_code(s, ProtocolCodes.REQUEST_CALL)
    answer = recv_code(s)
    if answer == ProtocolCodes.ACCEPT_CALL:
        start_streaming()
    else:
        stop_call()

def update_request_method(new_method : function):
    global accept_request_method
    accept_request_method = new_method