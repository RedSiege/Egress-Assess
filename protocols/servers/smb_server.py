'''

This is the code for the web server

'''

from impacket import smbserver


class Server:

    def __init__(self, cli_object):
        self.protocol = "smb"

    def serve(self):
        try:

            server = smbserver.SimpleSMBServer()

            server.addShare("DATA", "data/", "Data Chris share")

            # If you don't want log to stdout, comment the following line
            # If you want log dumped to a file, enter the filename
            server.setLogFile('')

            # Rock and roll
            server.start()
        # handle keyboard interrupts
        except KeyboardInterrupt:
            print "[!] Rage quiting, and stopping the web server!"
        return
