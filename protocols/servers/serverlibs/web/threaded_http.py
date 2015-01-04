from BaseHTTPServer import HTTPServer
from SocketServer import ThreadingMixIn


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass
