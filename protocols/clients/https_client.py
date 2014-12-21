'''

This is the web client code

'''


class Client:

    def __init__(self, cli_object):
        # Really http and https
        self.data_to_transmit = ''
        self.remote_server = cli_object.ip
        self.protocol = "https"

    def transmit(self, data_to_transmit):
        # Create the url to post to
        url = "https://" + self.remote_server + "post_data.php"

        # Post the data to the web server at the specified URL
        try:
            f = urllib2.urlopen(url, data_to_transmit)
            f.close()
            print "[*] File sent!!!"
        except urllib2.URLError:
            print "[*] Error: Web server may not be active on " + self.remote_server
            print "[*] Error: Please check server to make sure it is active!"
            sys.exit()
        return
