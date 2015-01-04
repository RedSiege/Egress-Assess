'''

This is the ftp client code

'''

import os
import socket
import sys
from common import helpers
from ftplib import FTP
from ftplib import error_perm


class Client:

    def __init__(self, cli_object):
        self.protocol = "ftp"
        self.remote_server = cli_object.ip
        self.username = cli_object.username
        self.password = cli_object.password

    def transmit(self, data_to_transmit):

        try:
            ftp = FTP(self.remote_server)
        except socket.gaierror:
            print "[*] Error: Cannot connect to FTP server.  Checking provided ip!"
            sys.exit()

        try:
            ftp.login(self.username, self.password)
        except error_perm:
            print "[*] Error: Username or password is incorrect!  Please re-run."
            sys.exit()

        ftp_file_name = helpers.writeout_text_data(data_to_transmit)

        ftp.storlines(
            "STOR " + ftp_file_name, open(helpers.ea_path()
                    + "/" + ftp_file_name))
        ftp.quit()
        os.remove(helpers.ea_path() + "/" + ftp_file_name)
        print "[*] File sent!!!"
