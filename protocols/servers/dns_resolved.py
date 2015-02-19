'''

This is a DNS Listening/server module that listens for requests, and 
writes out data within TXT requests to a file

'''

import base64
import time
from common import helpers
from scapy.all import *


class Server:

    def __init__(self, cli_object):

        self.protocol = "dns_resolved"
        self.last_packet = ''
        self.file_name = ''
        self.loot_path = ''

    def customAction(self, packet):

        if packet.haslayer(DNSQR):
            dnsqr_strings = repr(packet[DNSRR])
            try:
                print dnsqr_strings
            except TypeError:
                pass
        return

    def serve(self):

        self.loot_path = os.path.join(helpers.ea_path(), "data") + "/"
        # Check to make sure the agent directory exists, and a loot
        # directory for the agent.  If not, make them
        if not os.path.isdir(self.loot_path):
            os.makedirs(self.loot_path)

        # Get the date info
        current_date = time.strftime("%m/%d/%Y")
        current_time = time.strftime("%H:%M:%S")
        self.file_name = current_date.replace("/", "") +\
            "_" + current_time.replace(":", "") + "text_data.txt"

        print "[*] DNS server started!"
        sniff(prn=self.customAction)
        return
