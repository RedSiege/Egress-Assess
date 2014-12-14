'''

This is the code for the web server

'''

import ssl
from common import helpers
from serverlibs import base_handler
from serverlibs import threaded_http
from threading import Thread


class Server:

    def __init__(self):
        # This is really http and https
        self.protocol = "http"

    def serve(self):
        try:
            print "[*] Starting web server..."
            # bind to all interfaces
            Thread(target=self.serve_on_port, args=[443]).start()
            Thread(target=self.serve_on_port, args=[80]).start()
            print "[*] Web server is currently running"
            print "[*] Type \"killall -9 python\" to stop the web server."
        # handle keyboard interrupts
        except KeyboardInterrupt:
            print "[!] Rage quiting, and stopping the web server!"

    def serve_on_port(self, port):
        if port == 443:
            cert_path = helpers.ea_path() + '/protocols/servers/server.pem'
            server = threaded_http.ThreadingHTTPServer(
                ("0.0.0.0", port), base_handler.GetHandler)
            server.socket = ssl.wrap_socket(
                server.socket, certfile=cert_path, server_side=True)
            server.serve_forever()
        elif port == 80:
            server80 = threaded_http.ThreadingHTTPServer(
                ("0.0.0.0", port), base_handler.GetHandler)
            server80.serve_forever()
        return
