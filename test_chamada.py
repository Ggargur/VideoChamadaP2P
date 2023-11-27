import time
from vidstream import StreamingServer
from vidstream import CameraClient
from vidstream import AudioSender
from vidstream import AudioReceiver

import threading

s = CameraClient("10.42.0.184", 6666)
r = StreamingServer("0.0.0.0", 6666)

aas = AudioSender("10.42.0.184", 5555)
aar = AudioReceiver("0.0.0.0", 7777)

thread_listen = threading.Thread(target=r.start_server)
thread_listen.start()

thread_audio_listen = threading.Thread(target=aar.start_server)
thread_audio_listen.start()

time.sleep(2)

thread_send = threading.Thread(target=s.start_stream)
thread_send.start()

thread_audio_send = threading.Thread(target=aas.start_stream)
thread_audio_send.start()

while True:
    if input("") == "b":
        break
    continue


r.stop_server()
s.stop_stream()

aar.stop_server()
aas.stop_stream()