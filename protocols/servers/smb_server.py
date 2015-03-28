'''

This is the code for the web server

'''

import os
from impacket import smbserver


class Server:

    def __init__(self, cli_object):
        self.protocol = "smb"

    def serve(self):
        try:

            # current directory
            exfil_directory = os.path.join(os.getcwd(), "data")
            loot_path = exfil_directory + "/"

            # Check to make sure the agent directory exists, and a loot
            # directory for the agent.  If not, make them
            if not os.path.isdir(loot_path):
                os.makedirs(loot_path)

            server = smbserver.SimpleSMBServer()

            server.addShare("DATA", "data/", "Egress-Assess data share")

            # If you don't want log to stdout, comment the following line
            # If you want log dumped to a file, enter the filename
            server.setLogFile('')

            print "[*] SMB server is currently running..."

            # Rock and roll
            server.start()
        # handle keyboard interrupts
        except KeyboardInterrupt:
            print "[!] Rage quiting, and stopping the smb server!"
        return
