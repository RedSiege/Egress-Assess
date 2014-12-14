'''

This is the ftp client code

'''

import os
import socket
import sys
import time
from common import helpers
from ftplib import FTP
from ftplib import error_perm


class Client:

    def __init__(self, data_to_go, remote_system, user, passwd):
        self.protocol = "ftp"
        self.data_to_transmit = data_to_go
        self.remote_server = remote_system
        self.username = user
        self.password = passwd

    def transmit(self):

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
            # Create file name and write out file for ftp transfer
            current_date = time.strftime("%m/%d/%Y")
            current_time = time.strftime("%H:%M:%S")
            ftp_file_name = current_date.replace("/", "") +\
                "_" + current_time.replace(":", "") + "ftp_data.txt"

        with open(helpers.ea_path() + "/data/" + ftp_file_name, 'w') as cc_temp_file:
            cc_temp_file.write(self.data_to_transmit)

        ftp.storlines("STOR " + ftp_file_name, open(helpers.ea_path() + "/data/" + ftp_file_name))
        ftp.quit()
        os.remove(ftp_file_name)
        print "[*] File sent!!!"
