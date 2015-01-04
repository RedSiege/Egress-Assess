'''

This is a SMTP server module.  This was based on code made available at:
http://pymotw.com/2/smtpd/

'''

import asyncore
import os
import socket
import sys
from common import helpers
from protocols.servers.serverlibs.smtp import smtp_class


class Server:

    def __init__(self, cli_object):

        self.protocol = "smtp"

    def serve(self):

        exfil_directory = os.path.join(helpers.ea_path(), "data/")

        if not os.path.isdir(exfil_directory):
                os.makedirs(exfil_directory)

        print "[*] Started SMTP server..."

        try:
            smtp_server = smtp_class.CustomSMTPServer(('0.0.0.0', 25), None)
        except socket.error:
            print "[*] Error: Port 25 is currently in use!"
            print "[*] Error: Please re-start when not in use."
            sys.exit()

        try:
            asyncore.loop()
        except KeyboardInterrupt:
            print "[*] Shutting down SMTP server..."
            sys.exit()

        return
