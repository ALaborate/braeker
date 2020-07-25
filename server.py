import socket
import time

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
ENCODING = 'utf-8'
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    socket.setdefaulttimeout(0.5)
    s.listen(1)
    conn, addr = s.accept()
    data = None
    with conn:
        print('Connected by', addr)
        while True:
            time.sleep(2)
            try:
                data = conn.recv(1024)
            except socket.timeout:
                continue
            if not data:
                break
            print(data.decode(ENCODING), sep='', end='')
