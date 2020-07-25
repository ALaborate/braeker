import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1'
PORT = 7777
ENCODING = 'utf-8'

try:
    s.bind((HOST, PORT))
except OSError as err:
    print(f'Bind failed. Error: {str(err)}.')
    exit(err.errno)

print(f'Bind successful. Start listening on {PORT}.')
s.listen(10)

connection, address = s.accept()
print(f'Connected with {address[0]}:{str(address[1])}')
connection.sendall('State your name: '.encode(ENCODING))
data = connection.recv(1024)
reply = data.decode(ENCODING)
reply = '\nHello, '+reply+'!'
connection.sendall(reply.encode(ENCODING))
connection.close()
s.close()