'''

This is a ssh server designed to listen for sftp connections
This code came from:

base code came from - https://searchcode.com/codesearch/raw/53300304/

'''

import os
import paramiko
import socket
import threading
import time
from common import helpers
from StringIO import StringIO
from protocols.servers.serverlibs.sftp import sftp_classes


class Server:

    def __init__(self, cli_object):
        # self.protocol is the protocol that is viewable when using --list-servers
        # This is what the user would use along with --server.  It is the only
        # required attribute of the object.
        # You have complete access to command line arguments
        # within __init__
        # Anything that needs to be set for the server to run should have
        # a self attribute created within __init__
        self.protocol = "ssh"
        self.username = cli_object.username
        self.password = cli_object.password
        self.sftp_directory = helpers.ea_path() + '/data'
        self.port = 22

    def accept_client(self, client, addr, root_dir, users, host_rsa_key, password):
        usermap = {}
        for u in users:
            usermap[u.username] = u

        host_key_file = StringIO(host_rsa_key)
        host_key = paramiko.RSAKey(file_obj=host_key_file)
        transport = paramiko.Transport(client)
        transport.load_server_moduli()
        transport.add_server_key(host_key)

        impl = sftp_classes.SimpleSftpServer
        transport.set_subsystem_handler(
            "sftp", paramiko.SFTPServer, sftp_si=impl, transport=transport,
            fs_root=root_dir, users=usermap)

        server = sftp_classes.SimpleSSHServer(users=usermap)
        transport.start_server(server=server)
        channel = transport.accept()
        while(transport.is_active()):
            time.sleep(3)

        username = server.get_authenticated_user()
        if username is not None:
            user = usermap[username]
            os.system("svn commit -m 'committing user session for %s' %s" % (username, root_dir + "/" + user.home))

    # This is the main function that is called by the framework
    # You can build out as many different functions, but they all
    # need to be called from "serve".  If there is a specific function
    # or class that must be seperated out from this file (ideally keep
    # everything in here if possible), then add them to the serverlibs
    # directory
    def serve(self):

        loot_path = os.path.join(helpers.ea_path(), "data") + "/"
        # Check to make sure the agent directory exists, and a loot
        # directory for the agent.  If not, make them
        if not os.path.isdir(loot_path):
            os.makedirs(loot_path)

        user_map = [sftp_classes.User(username=self.username, password=self.password, chroot=False),]

        print "[*] Starting SFTP Server..."

        # read in the rsa key here
        with open(os.getcwd() + "/protocols/servers/serverlibs/sftp/key_file.txt", 'r') as rsa_key_file:
            key_dict = rsa_key_file.readlines()

        rsa_key = ''
        for line in key_dict:
            rsa_key = rsa_key + line.strip()

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', self.port))
        server_socket.listen(10)

        while True:
            client, addr = server_socket.accept()
            t = threading.Thread(target=self.accept_client, args=[
                client, addr, self.sftp_directory, user_map,
                rsa_key, self.password])
            t.start()

        return
