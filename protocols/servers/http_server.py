'''

This is the code for the web server

'''


class Server:

    def __init__(self, cli_object):
        self.protocol = "http"

    def serve(self):
        try:
            print "[*] Starting web (http) server..."
            # bind to all interfaces
            Thread(target=self.serve_on_port).start()
            print "[*] Web server is currently running"
            print "[*] Type \"killall -9 python\" to stop the web server."
        # handle keyboard interrupts
        except KeyboardInterrupt:
            print "[!] Rage quiting, and stopping the web server!"

    def serve_on_port(self):
        server80 = threaded_http.ThreadingHTTPServer(
            ("0.0.0.0", 80), base_handler.GetHandler)
        server80.serve_forever()
        return
