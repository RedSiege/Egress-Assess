'''

This is the code for the web server

'''


from SocketServer import ThreadingMixIn
from threading import Thread
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer

class Server:

    def __init__(self):
        # This is really http and https
        self.protocol = "http"

    def serve(self):
        pass
