'''

This is the code for the web server

'''

import os
import socket
import ssl
import sys
from common import helpers
from protocols.servers.serverlibs.web import base_handler
from protocols.servers.serverlibs.web import threaded_http
from threading import Thread


class Server:

    def __init__(self, cli_object):
        self.protocol = "https"
        if cli_object.server_port:
            self.port = int(cli_object.server_port)
        else:
            self.port = 443

    def serve(self):
        try:
            print "[*] Starting web (https) server..."
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
            cert_path = helpers.ea_path() +\
                '/protocols/servers/serverlibs/web/server.pem'
            server = threaded_http.ThreadingHTTPServer(
                ("0.0.0.0", self.port), base_handler.GetHandler)
            server.socket = ssl.wrap_socket(
                server.socket, certfile=cert_path, server_side=True)
            server.serve_forever()
        except socket.error:
            print "[*][*] Error: Port %d is currently in use!" % self.port
            print "[*][*] Error: Please restart when port is free!\n"
            sys.exit()
        return
