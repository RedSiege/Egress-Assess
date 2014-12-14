'''

This is the ftp client code

'''

from ftplib import FTP
from ftplib import error_perm


class Client:

    def __init__(self, data_to_go, remote_system):
        self.protocol = "ftp"
        self.data_to_transmit = data_to_go
        self.remote_server = remote_system

    def transmit(self):
        pass
