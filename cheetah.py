from wsgiref import simple_server
import os

class Cheetah:
    def __init__(self):
        self._cwd = os.getcwd()
        self._routes = {}
        self._error_route = None

    def listen(self, port=8000):
        server = simple_server.make_server("", port, self._app)
        server.serve_forever()

    def add_route(self, route, route_func):
        self._routes[route] = route_func

    def add_404(self, route_func):
        self._error_route = route_func

    def _app(self, environ, respond):
        if environ['PATH_INFO'] in self._routes:
            html_file = self._routes[environ['PATH_INFO']]()
            respond("200 OK", [("Content-Type", "text/html")])
            return html_file
        else:
            if self._error_route is not None:
                html_file = self._error_route()
                respond("200 OK", [("Content-Type", "text/html")])
                return html_file
            else:
                respond("404 Not Found", [("Content-Type", "text/plain")])
                return [b"404 Not Found"]
