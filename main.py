import socket

s = socket.socket()
server_addr = '127.0.0.1', 8000
s.bind(server_addr)
s.listen()


class Request:
    pass


def handle_request(request):
    if request.path == '/':
        return '<html><body>Hello <i>World!</i></body></html>'
    return 404, '<html><body><font color="red">Not Found</font></body></html>'


def handle_client(client):
    raw_request = client.recv(2048).decode().splitlines()
    request = Request()
    first_line = raw_request.pop(0)
    # METHOD /path HTTP/version
    request.method, request.path, request.http_version = first_line.split()
    request.http_version = request.http_version[len('HTTP/'):]

    request.headers = dict()
    while True:
        line = raw_request.pop(0)
        if not line:
            # reached the end of headers
            break
        name, colon, value = line.partition(': ')
        request.headers[name] = value

    result = handle_request(request)

    if isinstance(result, str):
        code = 200
        body = result
    else:
        code, body = result
    body = body.encode()

    code_name = {
        200: 'OK',
        404: 'Not Found'
    }[code]

    client.send('HTTP/1.0 {} {}\r\n'.format(code, code_name).encode())

    client.send(b'Server: Simple HTTP server 0.1\r\n')
    client.send(b'Content-Type: text/html\r\n')
    client.send('Content-Length: {}\r\n'.format(len(body)).encode())

    client.send(b'\r\n')
    client.send(body)

    client.close()


while True:
    s2, client_addr = s.accept()
    handle_client(s2)
