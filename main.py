import socket

s = socket.socket()
server_addr = '127.0.0.1', 8000
s.bind(server_addr)
s.listen()


class Request:
    pass


todo_list = []


def handle_request(request):
    if request.path == '/':
        return '''
        <html>
            <head>
                <title>To-do list</title>
            </head>
            <body>
                Your to-do list:
                <ul>
                    {}
                </ul>
            </body>
        </html>'''.format('\n'.join('<li>' + item + '</li>' for item in todo_list))

    if request.path == '/new' and request.method == 'POST':
        new_todo = request.body.strip()
        todo_list.append(new_todo)
        return 201, '<html><body>Created! Go back to the <a href="/">frontpage</a>.</body></html>'

    return 404, '<html><body><font color="red">Not Found</font></body></html>'


def parse_headers(raw_request):
    headers = dict()
    while True:
        line = raw_request.pop(0)
        if not line:
            # reached the end of headers
            break
        name, colon, value = line.partition(': ')
        headers[name] = value
    return headers


def handle_client(client):
    try:
        raw_request = client.recv(2048).decode().splitlines()
        request = Request()
        first_line = raw_request.pop(0)
        # METHOD /path HTTP/version
        request.method, request.path, request.http_version = first_line.split()
        request.http_version = request.http_version[len('HTTP/'):]

        request.headers = parse_headers(raw_request)
        request.body = '\n'.join(raw_request)

        result = handle_request(request)

        if isinstance(result, str):
            code = 200
            body = result
        else:
            code, body = result
        body = body.encode()

        code_name = {
            200: 'OK',
            201: 'Created',
            404: 'Not Found'
        }[code]

        client.send('HTTP/1.0 {} {}\r\n'.format(code, code_name).encode())

        client.send(b'Server: Simple HTTP server 0.1\r\n')
        client.send(b'Content-Type: text/html\r\n')
        client.send('Content-Length: {}\r\n'.format(len(body)).encode())

        client.send(b'\r\n')
        client.send(body)
    except:
        client.send(b'HTTP/1.0 500 Internal Server Error\r\n')
        client.send(b'\r\n')
    finally:
        client.close()


while True:
    s2, client_addr = s.accept()
    handle_client(s2)
