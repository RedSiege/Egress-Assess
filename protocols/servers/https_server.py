'''

This is the code for the web server

'''


class Server:

    def __init__(self, cli_object):
        self.protocol = "https"

    def serve(self):
        try:
            print "[*] Starting web (https) server..."
            # bind to all interfaces
            Thread(target=self.serve_on_port).start()
            print "[*] Web server is currently running"
            print "[*] Type \"killall -9 python\" to stop the web server."
        # handle keyboard interrupts
        except KeyboardInterrupt:
            print "[!] Rage quiting, and stopping the web server!"

    def serve_on_port(self):
        cert_path = helpers.ea_path() +\
            '/protocols/servers/serverlibs/server.pem'
        server = threaded_http.ThreadingHTTPServer(
            ("0.0.0.0", 443), base_handler.GetHandler)
        server.socket = ssl.wrap_socket(
            server.socket, certfile=cert_path, server_side=True)
        server.serve_forever()
        return
