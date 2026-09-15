import functools, os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
root = os.path.expanduser("~/ace-sites-v3/acedigitalservicesco-clone")
H = functools.partial(SimpleHTTPRequestHandler, directory=root)
H.log_message = lambda *a, **k: None
ThreadingHTTPServer(("127.0.0.1", 8799), H).serve_forever()
