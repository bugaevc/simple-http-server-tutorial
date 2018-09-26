import socket

s = socket.socket()
server_addr = '127.0.0.1', 8000
s.bind(server_addr)
s.listen()

while True:
    s2, client_addr = s.accept()
    s2.send(b'hello world\n')
    s2.close()
