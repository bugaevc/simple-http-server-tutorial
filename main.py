import socket


class NoHandlerError(Exception):
    pass


class Request:
    pass


class Handler:
    def can_handle(self, request):
        return False

    def handle(self, request):
        raise RuntimeError("abstract")


class Server:
    def __init__(self):
        self.s = socket.socket()
        server_addr = '127.0.0.1', 8000
        self.s.bind(server_addr)
        self.handlers = []

    def add_handler(self, handler):
        self.handlers.append(handler)

    def serve_forever(self):
        self.s.listen()
        while True:
            s2, client_addr = self.s.accept()
            try:
                self.handle_client(s2)
            except:
                s2.send(b'HTTP/1.0 500 Internal Server Error\r\n')
                s2.send(b'\r\n')
            finally:
                s2.close()

    def handle_client(self, client):
        raw_request = client.recv(2048).decode().splitlines()
        request = Request()
        first_line = raw_request.pop(0)
        # METHOD /path HTTP/version
        request.method, request.path, request.http_version = first_line.split()
        request.http_version = request.http_version[len('HTTP/'):]

        request.headers = self.parse_headers(raw_request)
        request.body = '\n'.join(raw_request)

        result = self.handle_request(request)

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

    def parse_headers(self, raw_request):
        headers = dict()
        while True:
            line = raw_request.pop(0)
            if not line:
                # reached the end of headers
                break
            name, colon, value = line.partition(': ')
            headers[name] = value
        return headers

    def handle_request(self, request):
        for handler in self.handlers:
            if handler.can_handle(request):
                return handler.handle(request)
        raise NoHandlerError()

class ToDo:
    def __init__(self):
        self.list = []

    def render_html(self):
        res = '<ul>'
        for item in self.list:
            res += '<li>' + item + '</li>'
        res += '</ul>'
        return res

    def add(self, item):
        self.list.append(item)


class RootHandler(Handler):
    def __init__(self, todo):
        self.todo = todo

    def can_handle(self, request):
        return request.path == '/' and request.method == 'GET'

    def handle(self, request):
        return '''
                <html>
                    <head>
                        <title>To-do list</title>
                    </head>
                    <body>
                        <p>Your to-do list:</p>
                        {}
                        <form action="/new" method="post">
                            <p>Add a new item:</p>
                            <input type="text" name="name" placeholder="Do stuff"/>
                            <input type="submit" value="Add"/>
                        </form>
                    </body>
                </html>'''.format(self.todo.render_html())


class NewHandler(Handler):
    def __init__(self, todo):
        self.todo = todo

    def can_handle(self, request):
        return request.path == '/new' and request.method == 'POST'

    def handle(self, request):
        new_todo = request.body.strip()
        new_todo = new_todo[len("name="):].replace('+', ' ')
        self.todo.add(new_todo)
        return 201, '<html><body>Created! Go back to the <a href="/">frontpage</a>.</body></html>'


class FourOhFourHandler(Handler):
    def can_handle(self, request):
        return True

    def handle(self, request):
        return 404, '<html><body><font color="red">Not Found</font></body></html>'


server = Server()
todo_list = ToDo()

server.add_handler(RootHandler(todo_list))
server.add_handler(NewHandler(todo_list))
server.add_handler(FourOhFourHandler())

server.serve_forever()
