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

    headers = dict()
    while True:
        line = request.pop(0)
        if not line:
            # reached the end of headers
            break
        name, colon, value = line.partition(': ')
        headers[name] = value


    if path == '/':
        code = 200
        body = '<html><body>Hello <i>World!</i></body></html>'
    else:
        code = 404
        body = '<html><body><font color="red">Not Found</font></body></html>'
    body = body.encode()

    code_name = {
        200: 'OK',
        404: 'Not Found'
    }[code]

    s2.send('HTTP/1.0 {} {}\r\n'.format(code, code_name).encode())

    s2.send(b'Server: Simple HTTP server 0.1\r\n')
    s2.send(b'Content-Type: text/html\r\n')
    s2.send('Content-Length: {}\r\n'.format(len(body)).encode())

    s2.send(b'\r\n')

    s2.send(body)

    s2.close()
