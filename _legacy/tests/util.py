import time
import re
import uuid
import socket


def new_log_in(c):
    name = str(uuid.uuid4())[:10]
    c.send(name)
    c.send("adasdadadsa")
    c.send("adasdadadsa")
    c.send("asdasad@adas.com")

def get_message(sock):
    # message = b''
    # while True:
    #     data = sock.recv(10240)
    #     if not data:
    #         break
    #     message += data
    return sock.recv(102400)

class Connection():
    def __enter__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(("localhost", 2112)) 
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._socket.__exit__()

    def send(self, s: str):
        print("> " + s)
        self._socket.sendall(s.encode())
        time.sleep(0.4)
        response = get_message(self._socket).decode()
        print(response)
        return response

def remove_control_chars(s: str) -> str:
    return re.sub(r'[\x00-\x1f]', '', s)

def check_end(s: str, end: str):
    return remove_control_chars(s).endswith(end)