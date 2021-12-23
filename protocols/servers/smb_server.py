'''

This is the code for the web server

'''

import os
from impacket import smbserver
from impacket.ntlm import compute_lmhash, compute_nthash

class Server:

    def __init__(self, cli_object):
        self.protocol = "smb"
        if cli_object.server_port:
           self.port = int(cli_object.server_port)
        else:
           self.port = 445

        self.smb2support = cli_object.smb2
        self.username=False
        self.password=False

        if cli_object.username and cli_object.password:
            self.username=cli_object.username
            self.password=cli_object.password
            self.lmhash=compute_lmhash(self.password)
            self.nthash=compute_nthash(self.password)

    def serve(self):
        try:

            # current directory
            exfil_directory = os.path.join(os.getcwd(), "data")
            loot_path = exfil_directory + "/"

            # Check to make sure the agent directory exists, and a loot
            # directory for the agent.  If not, make them
            if not os.path.isdir(loot_path):
                os.makedirs(loot_path)

            server = smbserver.SimpleSMBServer('0.0.0.0', self.port)
            if self.smb2support:
                server.setSMB2Support(self.smb2support)

            if self.username and self.password:
                server.addCredential(self.username, 0, self.lmhash, self.nthash)

            server.addShare("DATA", "data/", "Egress-Assess data share")

            # If you don't want log to stdout, comment the following line
            # If you want log dumped to a file, enter the filename
            server.setLogFile('')

            print("[*] SMB server is currently running...")

            # Rock and roll
            server.start()
        # handle keyboard interrupts
        except KeyboardInterrupt:
            print("[!] Rage quiting, and stopping the smb server!")
        return
