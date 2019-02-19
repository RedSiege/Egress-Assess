'''

This is a DNS Listening/server module that listens for requests, and 
writes out data within TXT requests to a file

'''

import base64
import time
import struct
import traceback
from common import helpers
from scapy.all import *


class Server:

    def __init__(self, cli_object):

        self.preamble = ".:|:."
        self.protocol = "dns"
        self.last_packet = ''
        self.file_name = ''
        self.loot_path = ''
        self.file_dict = {}
        self.file_status = ''

    def clearAttrs(self):
        self.last_packet = ''
        self.file_dict = {}
        self.file_status = ''
        self.setFileName()

    def setFileName(self):
        current_date = time.strftime("%m/%d/%Y")
        current_time = time.strftime("%H:%M:%S")
        self.file_name = current_date.replace("/", "") +\
            "_" + current_time.replace(":", "") + "text_data.txt"

    def parseQName(self, qr):
        return qr.get_field('qname').i2repr(qr, qr.qname)

    def parseDNSQR(self, packet):
        data = []
        dnsqr = packet.getlayer(DNSQR)
        #print(repr(dnsqr).split('<'))

        queries = [q.split(".")[0] for q in repr(dnsqr).split("qname='")[1:]]
        
        for txt in queries: 
            decoded = base64.b64decode(txt)
            parts = decoded.split(self.preamble)
            data.append({
                'txt_query': decoded,
                'file_status': str(struct.unpack(">I", parts[0])[0]),
                'file_data': parts[1]
            })


        return data

    def customAction(self, packet):

        if packet.haslayer(DNSQR):
            dnsqr_strings = repr(packet[DNSQR])

            if "ENDTHISFILETRANSMISSIONEGRESSASSESS" in dnsqr_strings:
                self.writeFile(dnsqr_strings)

            else:
                data = self.parseDNSQR(packet)
                sys.stdout.write('.')
                sys.stdout.flush()
                for d in data:
                    self.extractData(d['txt_query'], d['file_status'], d['file_data'], dnsqr_strings, packet)
        return

    def writeFile(self, dnsqr_strings):
        self.file_name = dnsqr_strings.split('\'')[1].rstrip('.').split('ENDTHISFILETRANSMISSIONEGRESSASSESS')[1]

        if self.file_status != '':
            print()
            helpers.received_file(self.file_name)

            with open(self.loot_path + self.file_name, 'w') as dns_out:
                for dict_key in xrange(1, int(self.file_status) + 1):
                    content = self.file_dict[str(dict_key)]
                    dns_out.write(content)

        # Clear out the class attributes after file upload is complete
        self.clearAttrs()

    def extractData(self, txt_query, file_status, file_data, dnsqr_strings, packet):
        try:
            if self.preamble in txt_query:
                self.file_status = file_status

                if self.file_status in self.file_dict:
                    pass
                else:
                    self.file_dict[self.file_status] = file_data

                    outgoing_data = self.file_status + "allgoodhere"

                    # This function from http://bb.secdev.org/scapy/issue/500/les-r-ponses-dns-de-type-txt-sont-malform
                    for i in range(0, len(outgoing_data), 0xff+1):
                        outgoing_data = outgoing_data[:i] + chr(len(outgoing_data[i:i+0xff])) + outgoing_data[i:]

                    #send(IP(dst=packet[IP].src)/UDP(dport=packet[UDP].sport, sport=53)/DNS(id=packet[DNS].id, qr=1,
                    #    qd=[DNSQR(qname=dnsqr_strings.split('\'')[1].rstrip('.'), qtype=packet[DNSQR].qtype)],
                    #    an=[DNSRR(rrname=dnsqr_strings.split('\'')[1].rstrip('.'), rdata=outgoing_data, type=packet[DNSQR].qtype)]),
                    #    verbose=False)

            else:
                # Write the entire Raw TXT query to a file
                with open(self.loot_path + self.file_name, 'a') as dns_out:
                    dns_out.write(txt_query)

                self.last_packet = txt_query

        except TypeError as e:
            print "[*] Potentially received a malformed DNS packet!"
            print traceback.format_exc()

    def serve(self):

        self.loot_path = os.path.join(helpers.ea_path(), "data") + "/"
        # Check to make sure the agent directory exists, and a loot
        # directory for the agent.  If not, make them
        if not os.path.isdir(self.loot_path):
            os.makedirs(self.loot_path)

        # Get the date info
        self.setFileName()

        print "[*] DNS server started!"
        sniff(prn=self.customAction, store=0)
        return
