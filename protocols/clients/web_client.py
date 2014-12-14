'''

This is the web client code

'''

import sys
import urllib2


class Client:

    def __init__(self, proto, data_to_go, remote_system):
        # Really http and https
        self.protocol = proto
        self.data_to_transmit = data_to_go
        self.remote_server = remote_system

    def transmit(self):
        # Create the url to post to
        if self.protocol.lower() == "http":
            url = "http://" + self.remote_server + "/post_data.php"
        elif self.protocol.lower() == "https":
            url = "https://" + self.remote_server + "post_data.php"
        else:
            print "[*] Error: Odd error, check web protocol being used!"
            sys.exit()

        # Post the data to the web server at the specified URL
        try:
            f = urllib2.urlopen(url, self.data_to_transmit)
            f.close()
            print "[*] File sent!!!"
        except urllib2.URLError:
            print "[*] Error: Web server may not be active on " + self.remote_server
            print "[*] Error: Please check server to make sure it is active!"
            sys.exit()
        return
