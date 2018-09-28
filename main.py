import socket

s = socket.socket()
server_addr = '127.0.0.1', 8000
s.bind(server_addr)
s.listen()

while True:
    s2, client_addr = s.accept()

    s2.send(b'HTTP/1.0 200 OK\r\n')

    s2.send(b'Server: Simple HTTP server 0.1\r\n')
    s2.send(b'Content-Type: text/plain\r\n')

    s2.send(b'\r\n')

    s2.send(b'hello world\n')

    s2.close()
