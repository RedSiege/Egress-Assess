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

        self.protocol = "dns"
        self.last_packet = ''
        self.file_name = ''
        self.loot_path = ''
        self.file_dict = {}
        self.total_packets = ''

    def customAction(self, packet):

        if packet.haslayer(DNSQR):
            print "got packet"
            dnsqr_strings = repr(packet[DNSQR])
            try:
                incoming_data = base64.b64decode(dnsqr_strings.split('\'')[1].rstrip('.'))
                self.file_name = incoming_data.split(".:|:.")[0]
                file_status = incoming_data.split(".:|:.")[1]
                file_data = incoming_data.split(".:|:.")[2]
                self.total_packets = file_status.split('/')[1]
                if file_status.split('/')[0] in self.file_dict:
                    pass
                else:
                    if ".:|:." in incoming_data:
                        self.file_dict[file_status.split('/')[0]] = file_data

                        outgoing_data = file_status.split('/')[0] + "allgoodhere"

                        # This function from http://bb.secdev.org/scapy/issue/500/les-r-ponses-dns-de-type-txt-sont-malform
                        for i in range(0, len(outgoing_data), 0xff+1):
                            outgoing_data = outgoing_data[:i] + chr(len(outgoing_data[i:i+0xff])) + outgoing_data[i:]

                        send(IP(dst=packet[IP].src)/UDP(dport=packet[UDP].sport, sport=53)/DNS(id=packet[DNS].id, qr=1,
                            qd=[DNSQR(qname=dnsqr_strings.split('\'')[1].rstrip('.'), qtype=packet[DNSQR].qtype)],
                            an=[DNSRR(rrname=dnsqr_strings.split('\'')[1].rstrip('.'), rdata=outgoing_data, type=packet[DNSQR].qtype)]),
                            verbose=False)
                        print "sent response packet"

                    else:
                        with open(self.loot_path + self.file_name, 'a') as dns_out:
                            dns_out.write(incoming_data)
                        self.last_packet = incoming_data
            except TypeError:
                if "ENDTHISFILETRANSMISSIONEGRESSASSESS" in dnsqr_strings:
                    print len(self.file_dict)
                    print str(self.total_packets)
                    with open(self.loot_path + self.file_name, 'a') as\
                            dns_out:
                        for dict_key in xrange(1, int(self.total_packets) + 1):
                            if str(dict_key) == '982':
                                print self.file_dict[str(dict_key)]
                            dns_out.write(self.file_dict[str(dict_key)])
                    sys.exit()
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
        sniff(prn=self.customAction, store=0)
        return
