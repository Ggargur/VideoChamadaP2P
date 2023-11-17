from vidstream import StreamingServer
import vidstream
import threading

def start_listening():
    server = StreamingServer('0.0.0.0', 9999)
    audio_listener = vidstream.AudioReceiver("0.0.0.0", 9998)

    audio_listener.start_server()
    server.start_server()

def start_streamer():
    video_streamer = vidstream.CameraClient('0.0.0.0', 9999)
    audio_streamer = vidstream.AudioSender("0.0.0.0",9998)
    
    audio_streamer.start_stream()
    video_streamer.start_stream()


streamer = threading.Thread(target=start_streamer)
streamer.start()
listener = threading.Thread(target=start_listening)
listener.start()