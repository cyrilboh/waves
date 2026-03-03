import os
from http.server import HTTPServer, BaseHTTPRequestHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MIME = {
    '.html': 'text/html',
    '.css':  'text/css',
    '.js':   'application/javascript',
    '.ico':  'image/x-icon',
    '.png':  'image/png',
}

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # silence access logs

    def do_GET(self):
        path = self.path.split('?')[0]
        if path == '/' or path == '':
            path = '/index.html'

        file_path = os.path.join(BASE_DIR, path.lstrip('/'))
        ext = os.path.splitext(file_path)[1]
        content_type = MIME.get(ext, 'text/plain')

        if os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                data = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(data))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not found')

if __name__ == '__main__':
    print('Starting waves on port 8254')
    HTTPServer(('127.0.0.1', 8254), Handler).serve_forever()
