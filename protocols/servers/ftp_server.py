'''

This is the code for the ftp server

'''

import os
import sys
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


class Server:

    def __init__(self):
        self.protocol = "ftp"
        self.username = ""
        self.password = ""
        self.data_directory = ""

    def serve(self):
        # current directory
        exfil_directory = os.path.join(os.getcwd(), "data")
        loot_path = exfil_directory + "/"

        # Check to make sure the agent directory exists, and a loot
        # directory for the agent.  If not, make them
        if not os.path.isdir(loot_path):
            os.makedirs(loot_path)

        try:
            authorizer = DummyAuthorizer()
            authorizer.add_user(
                self.username, self.password,
                loot_path, perm="lrw")

            handler = FTPHandler
            handler.authorizer = authorizer

            # Define a customized banner (string returned when client connects)
            handler.banner = "Connecting to Egress-Assess's FTP server!"

            server = FTPServer(('', 21), handler)
            server.serve_forever()
        except ValueError:
            print "[*] Error: The directory you provided may not exist!"
            print "[*] Error: Please re-run with a valid FTP directory."
            sys.exit()
        return
