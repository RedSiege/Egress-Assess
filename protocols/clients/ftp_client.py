'''

This is the ftp client code

'''

import time
from ftplib import FTP
from ftplib import error_perm


class Client:

    def __init__(self, data_to_go, remote_system):
        self.protocol = "ftp"
        self.data_to_transmit = data_to_go
        self.remote_server = remote_system

    def transmit(self):
        # Create file name and write out file for ftp transfer
        current_date = time.strftime("%m/%d/%Y")
        current_time = time.strftime("%H:%M:%S")
        ftp_file_name = current_date.replace("/", "") +\
            "_" + current_time.replace(":", "") + "ftp_data.txt"
