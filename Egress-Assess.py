#!/usr/bin/env python

# This tool is designed to be an easy way to test exfiltrating data
# from the network you are currently plugged into.  Used for red or
# blue teams that want to test network boundary egress detection
# capabilities.


import argparse
import sys
from common import helpers
from common import orchestra


def cli_parser():
    # Command line argument parser
    parser = argparse.ArgumentParser(
        add_help=False,
        description="The Egress-Assess is a tool used to assess egress filters\
        protecting a network")
    parser.add_argument(
        '-h', '-?', '--h', '-help', '--help', action="store_true",
        help=argparse.SUPPRESS)

    protocols = parser.add_argument_group('Client Protocol Options')
    protocols.add_argument(
        "--client", default=None, metavar="[http]",
        help="Extract data over the specified protocol.")
    protocols.add_argument(
        "--list-clients", default=False, action='store_true',
        help="List all supported client protocols.")
    protocols.add_argument("--ip", metavar="192.168.1.2", default=None,
                           help="IP to extract data to.")

    servers = parser.add_argument_group('Server Protocol Options')
    servers.add_argument(
        "--server", default=None, metavar='[http]',
        help="Create a server for the specified protocol.")
    servers.add_argument("--list-servers", default=False, action='store_true',
                         help="Lists all supported server protocols.")

    ftp_options = parser.add_argument_group('FTP Options')
    ftp_options.add_argument(
        "--username", metavar="testuser", default=None,
        help="Username for FTP server authentication.")
    ftp_options.add_argument(
        "--password", metavar="pass123", default=None,
        help="Password for FTP server authentication.")

    data_content = parser.add_argument_group('Data Content Options')
    data_content.add_argument(
        "--data-size", default=1, type=int,
        help="Number of megs to send")
    data_content.add_argument(
        "--ssn", default=False, action='store_true',
        help="Extract data containing fake social security numbers.")
    data_content.add_argument(
        '--cc', default=False, action='store_true',
        help="Extract data containing fake credit card numbers")

    args = parser.parse_args()

    if args.h:
        parser.print_help()
        sys.exit()

    if (args.server == "ftp") and (args.username is None or args.password is None):
        print "[*] Error: FTP Server requires a username and password!"
        print "[*] Error: Please re-run and provide the required info!"
        sys.exit()

    if (args.client) and args.ip is None:
        print "[*] Error: You said to act like a client, but provided no ip"
        print "[*] Error: to connect to.  Please re-run with required info!"
        sys.exit()

    if (args.client is not None) and (args.cc is False and args.ssn is False):
        print "[*] Error: You need to tell Egress-Assess the type of data to send!"
        print "[*] Error: to connect to.  Please re-run with required info!"
        sys.exit()

    if (args.client is None and args.server is None and
            args.list_servers is None and args.list_clients is None):
        print "[*] Error: You didn't tell Egress-Assess to act like \
            a server or client!".replace('    ', '')
        print "[*] Error: Please re-run and provide an action to perform!"
        parser.print_help()
        sys.exit()

    return args


if __name__ == "__main__":

    helpers.title_screen()

    cli_parsed = cli_parser()

    the_conductor = orchestra.Conductor()

    if cli_parsed.server is not None:
        the_conductor.load_server_protocols(cli_parsed)
        for full_path, server in the_conductor.server_protocols.iteritems():
            if server.protocol == cli_parsed.server.lower():
                server.serve()

    elif cli_parsed.client is not None:
        the_conductor.load_client_protocols(cli_parsed)
        the_conductor.load_datatypes(cli_parsed)
