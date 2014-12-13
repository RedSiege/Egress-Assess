'''

This is the code for the ftp server

'''

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


class Server:

    def __init__(self):
        self.protocol = "ftp"

    def serve(self):
        pass
