import socket

s = socket.socket()
server_addr = '127.0.0.1', 8000
s.bind(server_addr)
s.listen()

while True:
    s2, client_addr = s.accept()

    request = s2.recv(2048).decode().splitlines()
    first_line = request.pop(0)
    # METHOD /path HTTP/version
    method, path, http_version = first_line.split()
    http_version = http_version[len('HTTP/'):]

    if path == '/':
        code = 200
        code_name = 'OK'
        body = 'hello world!'
    else:
        code = 404
        code_name = 'Not Found'
        body = 'not found'

    s2.send('HTTP/1.0 {} {}\r\n'.format(code, code_name).encode())

    s2.send(b'Server: Simple HTTP server 0.1\r\n')
    s2.send(b'Content-Type: text/plain\r\n')

    s2.send(b'\r\n')

    s2.send(body.encode())

    s2.close()
