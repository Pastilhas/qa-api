import json
from engine import engine
from http.server import BaseHTTPRequestHandler, HTTPServer


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes("Send a POST with query as string", "utf-8"))

    def do_POST(self):
        _len = int(self.headers['Content-Length'])
        q = self.rfile.read(_len).decode("utf-8")

        a = engine.ask(q)

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes(json.dumps({"query": q, "answer": a}), "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer(('0.0.0.0', 8000), MyServer)
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
