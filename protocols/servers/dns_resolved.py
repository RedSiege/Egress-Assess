'''

This is a DNS Listening/server module that listens for requests, and 
writes out data within A record requests to a file

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
        self.file_dict = {}
        self.file_name = ''
        self.file_status = ''

    def customAction(self, packet):

        if packet.haslayer(UDP) and packet.haslayer(DNSQR):
            dnsqr_strings = repr(packet[DNSQR])
            if "file---" in dnsqr_strings:
                self.file_name = dnsqr_strings.split('\'')[1].rstrip('.').split('file---')[1]
                with open(self.loot_path + self.file_name, 'a') as\
                        dns_out:
                    for dict_key in xrange(1, int(self.file_status) + 1):
                        dns_out.write(self.file_dict[str(dict_key)])
                sys.exit()
            else:
                try:
                    string_to_decode = dnsqr_strings.split('\'')[1].rstrip('.').split('.')[0]
                    if '-pqp-' in string_to_decode:
                        string_to_decode = string_to_decode.replace('-pqp-', '=')
                    incoming_data = base64.b64decode(string_to_decode)
                    if ".:|:." in incoming_data:
                        self.file_status = incoming_data.split('.:|:.')[0]
                        file_data = incoming_data.split('.:|:.')[1]
                        self.file_dict[self.file_status] = file_data

                        outgoing_data = self.file_status + "allgoodhere"

                        # This function from http://bb.secdev.org/scapy/issue/500/les-r-ponses-dns-de-type-txt-sont-malform
                        for i in range(0, len(outgoing_data), 0xff+1):
                            outgoing_data = outgoing_data[:i] + chr(len(outgoing_data[i:i+0xff])) + outgoing_data[i:]

                        send(IP(dst=packet[IP].src)/UDP(dport=packet[UDP].sport, sport=53)/DNS(rd=1, id=packet[DNS].id, qr=1,
                            qd=[DNSQR(qname=dnsqr_strings.split('\'')[1].rstrip('.'), qtype=packet[DNSQR].qtype)],
                            an=[DNSRR(rrname=dnsqr_strings.split('\'')[1].rstrip('.'), rdata=outgoing_data, type=packet[DNSQR].qtype)]),
                            verbose=False)

                    else:
                        with open(self.loot_path + self.file_name, 'a') as dns_out:
                            dns_out.write(encoded_data)
                        self.last_packet = encoded_data

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
