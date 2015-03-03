'''

This is the code for the web server

'''

import os
import socket
import sys
from protocols.servers.serverlibs.web import base_handler
from protocols.servers.serverlibs.web import threaded_http
from threading import Thread


class Server:

    def __init__(self, cli_object):
        self.protocol = "http"

    def serve(self):
        try:
            print "[*] Starting web (http) server..."
            # bind to all interfaces
            Thread(target=self.serve_on_port).start()
            print "[*] Web server is currently running"
            print "[*] Type \"kill -9 " + str(os.getpid()) + "\" to stop the web server."
        # handle keyboard interrupts
        except KeyboardInterrupt:
            print "[!] Rage quiting, and stopping the web server!"
        return

    def serve_on_port(self):
        try:
            server80 = threaded_http.ThreadingHTTPServer(
                ("0.0.0.0", 80), base_handler.GetHandler)
            server80.serve_forever()
        except socket.error:
            print "[*][*] Error: Port 80 is currently in use!"
            print "[*][*] Error: Please restart when port is free!\n"
            sys.exit()
        return
