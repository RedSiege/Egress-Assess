'''

This is the web client code

'''

import sys
import urllib2


class Client:

    def __init__(self, cli_object):
        self.data_to_transmit = ''
        self.remote_server = cli_object.ip
        self.protocol = "http"
        if cli_object.client_port is None:
            self.port = 80
        else:
            self.port = cli_object.client_port
        if cli_object.file is None:
            self.file_transfer = False
        else:
            if "/" in cli_object.file:
                self.file_transfer = cli_object.file.split("/")[-1]
            else:
                self.file_transfer = cli_object.file

    def transmit(self, data_to_transmit):

        if not self.file_transfer:
            url = "http://" + self.remote_server + ":" + str(self.port) + "/post_data.php"

            # Post the data to the web server at the specified URL
            try:
                f = urllib2.urlopen(url, data_to_transmit)
                f.close()
                print "[*] File sent!!!"
            except urllib2.URLError:
                print "[*] Error: Web server may not be active on " + self.remote_server
                print "[*] Error: Please check server to make sure it is active!"
                sys.exit()
        else:
            url = "http://" + self.remote_server + ":" + str(self.port) + "/post_file.php"

            try:
                data_to_transmit = self.file_transfer + ".:::-989-:::." + data_to_transmit
                f = urllib2.urlopen(url, data_to_transmit)
                f.close()
                print "[*] File sent!!!"
            except urllib2.URLError:
                print "[*] Error: Web server may not be active on " + self.remote_server
                print "[*] Error: Please check server to make sure it is active!"
                sys.exit()

        return
