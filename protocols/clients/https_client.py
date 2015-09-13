'''

This is the web client code

'''

import ssl
import sys
import urllib2


class Client:

    def __init__(self, cli_object):
        self.data_to_transmit = ''
        self.remote_server = cli_object.ip
        self.protocol = "https"
        if cli_object.file is None:
            self.file_transfer = False
        else:
            if "/" in cli_object.file:
                self.file_transfer = cli_object.file.split("/")[-1]
            else:
                self.file_transfer = cli_object.file

    def transmit(self, data_to_transmit):
        # This restores the same behavior as before.
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            # Legacy Python that doesn't verify HTTPS certificates by default
            pass
        else:
            # Handle target environment that doesn't support HTTPS verification
            ssl._create_default_https_context = _create_unverified_https_context
        if not self.file_transfer:
            url = "https://" + self.remote_server + "/post_data.php"

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
            url = "https://" + self.remote_server + "/post_file.php"

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
