#!/usr/bin/env python

# This tool is designed to be an easy way to test exfiltrating data
# from the network you are currently plugged into.  Used for red or
# blue teams that want to test network boundary egress detection
# capabilities.


import argparse
import sys
from common import helpers


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
        "--ftp", default=False, action='store_true',
        help="Extract data over FTP.")
    protocols.add_argument("--http", default=False, action='store_true',
                           help="Extract data over http.")
    protocols.add_argument("--https", default=False, action='store_true',
                           help="Extract data over https.")
    protocols.add_argument("--ip", metavar="192.168.1.2", default=None,
                           help="IP to extract data to.")

    servers = parser.add_argument_group('Server Protocol Options')
    servers.add_argument(
        "--ftp-server", default=False, action='store_true',
        help="FTP Server that receives client data.")
    servers.add_argument("--http-server", default=False, action='store_true',
                         help="HTTP and HTTPS server, receives POST data.")

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

    # If using FTP, check to make sure a username and pass is provided
    if args.ftp and (args.password is None or args.username is None):
        print "[*] Error: FTP Server requires a username and password!"
        print "[*] Error: Please re-run and provide the required info!"
        sys.exit()

    if (args.ftp or args.http or args.https) and args.ip is None:
        print "[*] Error: You said to act like a client, but provided no ip"
        print "[*] Error: to connect to.  Please re-run with required info!"
        sys.exit()

    if not (
        args.ftp or args.http or args.https or args.http_server or
            args.ftp_server):
        print "[*] Error: You didn't tell Egress-Assess to act like\
            a server or client!".replace('    ', '')
        print "[*] Error: Please re-run and provide an action to perform!"
        sys.exit()

    return args


if __name__ == "__main__":

    helpers.title_screen()

    cli_parsed = cli_parser()
