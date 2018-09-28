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


while True:
    s2, client_addr = s.accept()

    raw_request = s2.recv(2048).decode().splitlines()
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

    s2.send('HTTP/1.0 {} {}\r\n'.format(code, code_name).encode())

    s2.send(b'Server: Simple HTTP server 0.1\r\n')
    s2.send(b'Content-Type: text/html\r\n')
    s2.send('Content-Length: {}\r\n'.format(len(body)).encode())

    s2.send(b'\r\n')

    s2.send(body)

    s2.close()
