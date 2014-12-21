'''

This is the conductor which controls everything

'''

import glob
import imp


class Conductor:

    def __init__(self):
        # Create dictionaries of supported modules
        # empty until stuff loaded into them
        self.client_protos = {}
        self.server_protos = {}
        self.data = {}

    def load_client_protocols(self):
        for name in glob.glob('protocols/clients/*.py'):
            if name.endswith("__init__.py"):
                pass
            elif name.endswith(".pyc"):
                pass
            else:
                print name
        return


    def load_server_protocols(self):
        self.server_protos = dict((name, imp.load_source(namem, name)) for name in glob.glob('protocols/servers/*.py'))

    def load_datatypes(self):
        self.data = dict((name, imp.load_source(name, name)) for name in glob.glob('datatypes/*.py'))

    def print_client_proto(self):
        print self.client_protos
        return