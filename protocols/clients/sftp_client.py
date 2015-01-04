'''

This is the template that should be used for client modules.
A brief description of the client module can/should be placed
up here.  All necessary imports should be placed between the
comments and class declaration.

Finally, be sure to rename your client module to a .py file

'''

import paramiko
import os
from common import helpers


class Client:

    def __init__(self, cli_object):
        self.protocol = "sftp"
        self.username = cli_object.username
        self.password = cli_object.password
        self.remote_system = cli_object.ip

    def transmit(self, data_to_transmit):

        print "[*][*] WARNING: Currently only works with root user account!"
        print "[*][*] WARNING: This should be fixed when SFTP server module \
            is released!".replace('    ', '')

        print "[*] Transmitting data..."

        sftp_file_name = helpers.writeout_text_data(data_to_transmit)
        full_path = helpers.ea_path() + "/" + sftp_file_name

        transport = paramiko.Transport(self.remote_system)
        transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(full_path, '/' + sftp_file_name)

        # close sftp connection
        sftp.close()
        transport.close()

        os.remove(sftp_file_name)

        print "[*] Data sent!"

        return
