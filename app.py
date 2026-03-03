from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"waves is running")

if __name__ == "__main__":
    print(f"Starting waves on port 8254")
    HTTPServer(("127.0.0.1", 8254), Handler).serve_forever()
