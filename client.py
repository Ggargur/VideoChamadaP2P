from protocol import *
import socket
import stream.streaming as streaming
import stream.audio as audio
import threading

user_name = ""
client_names: list[str] = []
accept_request_method: callable

video_streamer: streaming.CameraClient = None
audio_streamer: audio.AudioSender = None

audio_listener: audio.AudioReceiver = None
streaming_server: streaming.StreamingServer = None

streamer_thread: threading.Thread = None
listener_thread: threading.Thread = None
request_thread: threading.Thread = None

is_running = True


# Conecta-se ao servidor.
def connect_server() -> socket.socket:
    SERVER_ADDRESS = ("0.0.0.0", SERVER_PORT)
    server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_conn.connect(SERVER_ADDRESS)
    return server_conn


# Prepara uma porta cliente para iniciar uma conexão com outro cliente.
def start_listening() -> socket.socket:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(("0.0.0.0", 0))
    s.listen()
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
def request_name(user_name: str) -> tuple[str, int]:
    server_conn = connect_server()

    send_code(server_conn, ProtocolCodes.REQUEST_ADDRESS)
    send_string(server_conn, user_name)

    status = recv_code(server_conn)
    if status == ProtocolCodes.NOT_FOUND:
        print(f"Endereço de {user_name} não encontrado")
        return ("Não encontrado", -1)
    host = desserialize_address(recv_int(server_conn))
    port = recv_int(server_conn, 2)

    print(f"Nome {user_name} está disponível em {host}:{port}")
    return (host, port)


# Retorna todos os nomes que um dado usuario cadastrou, ou seja, todos pertencentes a um mesmo ip.
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


# Inicializa as variaveis para envio de audio e video do stream, permitindo o fluxo que informacoes que sera enviado pelo
# outro usuario.
def start_listener_server():
    global audio_listener, streaming_server
    audio_listener = audio.AudioReceiver("0.0.0.0", 6666)
    streaming_server = streaming.StreamingServer("0.0.0.0", 9999)

    audio_listener.start_server()
    streaming_server.start_server()


# Coloca o inicia os métodos de ouvir a chamada em uma nova thread.
def start_listening_to_stream():
    global listener_thread
    listener_thread = threading.Thread(target=start_listener_server)
    listener_thread.start()


# Coloca o inicia os métodos de ouvir por requisições de novas chamadas.
def start_listening_to_requests(socket: socket.socket):
    global request_thread
    request_thread = threading.Thread(target=listen_to_requests, args=(socket,), daemon=True)
    request_thread.start()

# Inicializa as variaveis para recebimento de audio e video do stream, permitindo o fluxo que informacoes que sera enviado pelo
# outro usuario.
def start_streaming_server(address: str):
    global video_streamer, audio_streamer
    video_streamer = streaming.CameraClient(address, 9999)
    audio_streamer = audio.AudioSender(address, 6666)

    audio_streamer.start_stream()
    video_streamer.start_stream()

# Coloca o inicia os métodos de enviar vídeo e audio para uma chamada em uma nova thread.
def start_streaming(address: str):
    global streamer_thread
    streamer_thread = threading.Thread(target=start_streaming_server, args=(address,))
    streamer_thread.start()


# Finaliza as variaveis envolvidas no streaming de audio e video
# verificando se cada uma destas foram incializadas para enfim parar com a execucao de todas.
def stop_call():
    global video_streamer, audio_streamer, streaming_server, audio_listener
    if video_streamer is not None:
        video_streamer.stop_stream()
        video_streamer = None
    if audio_streamer is not None:
        audio_streamer.stop_stream()
        audio_streamer = None
    if audio_listener is not None:
        audio_listener.stop_server()
        audio_listener = None
    if streaming_server is not None:
        streaming_server.stop_server()
        streaming_server = None


# Metodo que permite um cliente "escutar" por requisicoes de videoconferencia.
def listen_to_requests(socket: socket.socket):
    global accept_request_method, is_running
    while is_running:
        (connection, address_conection) = socket.accept()
        code = recv_code(connection)
        if (code == ProtocolCodes.REQUEST_CALL):
            handle_connection_request(connection, address_conection)

# Começa uma chamada caso o usuário aceite conectar-se, caso contrário envia um sinal de conexão não aceita.
def handle_connection_request(connection: socket.socket, address: str):
    print("Me foi requesitada uma chamada.")
    if get_connection_accept_input(address):
        accept_call(connection)
    else:
        send_code(connection, ProtocolCodes.REFUSE_CALL)

# Pega o resultado do input do usuário quando ele é requisitado para saber se deseja aceitar uma chamada.
def get_connection_accept_input(address: str):
    if accept_request_method is not None:
        return accept_request_method(address)
    return True

# Aceita uma conexão de chamada com um usuário.
def accept_call(socket: socket.socket):
    start_listening_to_stream()
    send_code(socket, ProtocolCodes.ACCEPT_CALL)
    code = recv_code(socket)
    if code == ProtocolCodes.STARTED_STREAMING:
        start_streaming(socket.getpeername()[0])

# Tenta conectar-se com um novo usuário para começar uma chamada.
def connect_with(address: str, port: int):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((address, port))
        start_listening_to_stream()
        send_code(s, ProtocolCodes.REQUEST_CALL)
        answer = recv_code(s)
        if answer == ProtocolCodes.ACCEPT_CALL:
            start_streaming(address)
            send_code(s, ProtocolCodes.STARTED_STREAMING)
        else:
            stop_call()
    except:
        print("Não consegui me conectar com esse usuário.")
        stop_call()

# Altera o método que pede para o usuário se ele deseja aceitar uma nova conexão.
def update_request_method(new_method: callable):
    global accept_request_method
    accept_request_method = new_method


# incia processo de fim de uma chamada.
def quit_client():
    global listener_thread, streamer_thread, request_thread, is_running
    stop_call()
    is_running = False
