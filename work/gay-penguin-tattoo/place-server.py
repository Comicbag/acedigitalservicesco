#!/usr/bin/env python3
"""Tiny static server for the Gay Penguin placement editor.
Serves the project folder AND accepts POST /api/save -> writes jewelry/placements.json
so the editor's Save button persists a real file (the customer try-on reads it).
Run:  python3 place-server.py   then open  http://127.0.0.1:8131/place.html
"""
import http.server, socketserver, json, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
PORT = 8131

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/save':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                os.makedirs('jewelry', exist_ok=True)
                with open('jewelry/placements.json', 'w') as f:
                    json.dump(data, f, indent=2)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"ok":true}')
                print('saved placements.json (%d pieces)' % len(data))
            except Exception as e:
                self.send_response(500); self.end_headers(); self.wfile.write(str(e).encode())
        else:
            self.send_response(404); self.end_headers()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, *a):
        pass

with socketserver.TCPServer(('127.0.0.1', PORT), Handler) as httpd:
    print('Placement editor:  http://127.0.0.1:%d/place.html' % PORT)
    httpd.serve_forever()
