from engine import engine
from http.server import BaseHTTPRequestHandler, HTTPServer


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        q = self.path[1:]
        a = engine.ask(q)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(f"{{query:{q},answer:{a}}}", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer(('localhost', 8000), MyServer)
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
