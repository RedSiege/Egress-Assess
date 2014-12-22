'''

This is the conductor which controls everything

'''

import copy
import glob
import imp
import os
import random
import socket
import ssl
import sys
import time
import urllib2
from common import helpers
from ftplib import FTP
from ftplib import error_perm
from protocols.servers import *
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


class Conductor:

    def __init__(self):
        # Create dictionaries of supported modules
        # empty until stuff loaded into them
        self.client_protocols = {}
        self.server_protocols = {}
        self.datatypes = {}

    def load_client_protocols(self, command_line_object):
        for name in glob.glob('protocols/clients/*.py'):
            if name.endswith("__init__.py"):
                pass
            elif name.endswith(".pyc"):
                pass
            else:
                loaded_client_proto = imp.load_source(name.replace("/", ".").rstrip('.py'), name)
                self.client_protocols[name] = loaded_client_proto.Client(command_line_object)
        return


    def load_server_protocols(self, command_line_object):
        for name in glob.glob('protocols/servers/*.py'):
            if name.endswith("__init__.py"):
                pass
            elif name.endswith(".pyc"):
                pass
            else:
                loaded_server_proto = imp.load_source(name.replace("/", ".").rstrip('.py'), name)
                self.server_protocols[name] = loaded_server_proto.Server(command_line_object)
        return

    def load_datatypes(self, command_line_object):
        for name in glob.glob('datatypes/*.py'):
            if name.endswith("__init__.py"):
                pass
            elif name.endswith(".pyc"):
                pass
            else:
                loaded_datatypes = imp.load_source(name.replace("/", ".").rstrip('.py'), name)
                self.datatypes[name] = loaded_datatypes.Datatype(command_line_object)
        return
