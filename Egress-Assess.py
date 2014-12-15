#!/usr/bin/env python

# This tool is designed to be an easy way to test exfiltrating data
# from the network you are currently plugged into.  Used for red or
# blue teams that want to test network boundary egress detection
# capabilities.


import argparse
import copy
import os
import random
import socket
import ssl
import string
import sys
import time
import urllib2
from ftplib import FTP
from ftplib import error_perm
from SocketServer import ThreadingMixIn
from threading import Thread
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


class GetHandler(BaseHTTPRequestHandler):
    # Some of the http server code came from Dave Kennedy's AES shell
    # over http - the server specific code

    # should be performing GET requests Help from
    # http://pymotw.com/2/BaseHTTPServer/
    def do_GET(self):

        # 404 since we aren't serving up any pages, only receiving data
        self.send_response(404)
        self.end_headers()
        return

    # handle post request
    def do_POST(self):

        # Gather the Posted URI from the agent/browser
        # parsed_path = urlparse.urlparse(self.path)
        uri_posted = self.path
        uri_posted = uri_posted.replace("/", "")
        #incoming_ip = self.client_address[0]
        # current directory
        exfil_directory = os.path.join(os.getcwd(), "data")
        loot_path = exfil_directory + "/"

        # Info for this from -
        # http://stackoverflow.com/questions/13146064/simple-
        # python-webserver-to-save-file
        if uri_posted == "ccdata.php":

            self.send_response(200)
            self.end_headers()
            loot_path = exfil_directory + "/"

            # Check to make sure the agent directory exists, and a loot
            # directory for the agent.  If not, make them
            if not os.path.isdir(loot_path):
                os.makedirs(loot_path)

            # Get the date info
            current_date = time.strftime("%m/%d/%Y")
            current_time = time.strftime("%H:%M:%S")
            screenshot_name = current_date.replace("/", "") +\
                "_" + current_time.replace(":", "") + "ccdata.txt"

            # Read the length of the screenshot file being uploaded
            screen_length = self.headers['content-length']
            screen_data = self.rfile.read(int(screen_length))

            # Write out the file
            with open(loot_path + screenshot_name, 'w') as cc_data_file:
                cc_data_file.write(screen_data)

        elif uri_posted == "ssndata.php":
            self.send_response(200)
            self.end_headers()

            # Check to make sure the agent directory exists, and a loot
            # directory for the agent.  If not, make them
            if not os.path.isdir(loot_path):
                os.makedirs(loot_path)

            # Get the date info
            current_date = time.strftime("%m/%d/%Y")
            current_time = time.strftime("%H:%M:%S")
            screenshot_name = current_date.replace("/", "") +\
                "_" + current_time.replace(":", "") + "ssndata.txt"

            # Read the length of the screenshot file being uploaded
            screen_length = self.headers['content-length']
            screen_data = self.rfile.read(int(screen_length))

            # Write out the file
            with open(loot_path + screenshot_name, 'w') as cc_data_file:
                cc_data_file.write(screen_data)

        # All other Post requests
        else:

            self.send_response(404)
            self.end_headers()

            print "Odd... someone else is trying to access this web server..."
            print "Might want to check that out..."
        return


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass


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
        print "[*] Error: You didn't tell Egress-Assess to act like \
            a server or client!".replace('    ', '')
        print "[*] Error: Please re-run and provide an action to perform!\n\n"
        parser.print_help()
        sys.exit()

    return args


def completed_number(prefix, length, the_generator):
    """
    'prefix' is the start of the CC number as a string, any number of digits.
    'length' is the length of the CC number to generate. Typically 13 or 16
    """

    ccnumber = prefix

    # generate digits
    while len(ccnumber) < (length - 1):
        digit = str(the_generator.choice(range(0, 10)))
        ccnumber.append(digit)

    # Calculate sum
    sum = 0
    pos = 0

    reversedCCnumber = []
    reversedCCnumber.extend(ccnumber)
    reversedCCnumber.reverse()

    while pos < length - 1:
        odd = int(reversedCCnumber[pos]) * 2
        if odd > 9:
            odd -= 9

        sum += odd

        if pos != (length - 2):
            sum += int(reversedCCnumber[pos + 1])
        pos += 2

    # Calculate check digit
    checkdigit = ((sum / 10 + 1) * 10 - sum) % 10
    ccnumber.append(str(checkdigit))
    return ''.join(ccnumber)


def credit_card_number(prefixList, length, howMany):

    generator = random.Random()
    generator.seed()

    result = []

    while len(result) < howMany:
        ccnumber = copy.copy(generator.choice(prefixList))
        result.append(completed_number(ccnumber, length, generator))

    return result


def ftp_client_connect(command_line_object):
    # Create FTP objects that connects to the ftp server
    # with the provided username and password
    try:
        ftp = FTP(command_line_object.ip)
    except socket.gaierror:
        print "[*] Error: Cannot connect to FTP server.  Checking provided ip!"
        sys.exit()

    try:
        ftp.login(command_line_object.username, command_line_object.password)
    except error_perm:
        print "[*] Error: Username or password is incorrect!  Please re-run."
        sys.exit()

    # Create file to upload
    if command_line_object.ssn:
        # Get the date info
        current_date = time.strftime("%m/%d/%Y")
        current_time = time.strftime("%H:%M:%S")
        ftp_file_name = current_date.replace("/", "") +\
            "_" + current_time.replace(":", "") + "ssndata.txt"

        # Generate 150000 SSNs for http(s) transfer
        # This is about 1.9 megs
        ssns = ''
        for single_ssn in range(0, 81500 * command_line_object.data_size):
            ssns += generate_ssn() + ', '
        with open(os.getcwd() + "/" + ftp_file_name, 'w') as ssn_temp_file:
            ssn_temp_file.write(ssns)

    elif command_line_object.cc:
        # Get the date info
        current_date = time.strftime("%m/%d/%Y")
        current_time = time.strftime("%H:%M:%S")
        ftp_file_name = current_date.replace("/", "") +\
            "_" + current_time.replace(":", "") + "ccdata.txt"

        all_ccs = ''
        credit_cards = generate_credit_cards(command_line_object)
        for card in credit_cards:
            all_ccs += card + ', '
        with open(os.getcwd() + "/" + ftp_file_name, 'w') as cc_temp_file:
            cc_temp_file.write(all_ccs)

    ftp.storlines("STOR " + ftp_file_name, open(ftp_file_name))
    ftp.quit()
    os.remove(ftp_file_name)
    print "[*] File sent!!!"
    return


def ftp_server(command_line_object):
    # current directory
    exfil_directory = os.path.join(os.getcwd(), "data")
    loot_path = exfil_directory + "/"

    # Check to make sure the agent directory exists, and a loot
    # directory for the agent.  If not, make them
    if not os.path.isdir(loot_path):
        os.makedirs(loot_path)

    try:
        authorizer = DummyAuthorizer()
        authorizer.add_user(
            command_line_object.username, command_line_object.password,
            loot_path, perm="lrw")

        handler = FTPHandler
        handler.authorizer = authorizer

        # Define a customized banner (string returned when client connects)
        handler.banner = "Connecting to Egress-Assess's FTP server!"

        server = FTPServer(('', 21), handler)
        server.serve_forever()
    except ValueError:
        print "[*] Error: The directory you provided may not exist!"
        print "[*] Error: Please re-run with a valid FTP directory."
        sys.exit()


def generate_credit_cards(command_object):
    # Fake credit card generation code came from:
    # https://github.com/grahamking/darkcoding-credit-card

    # credit card constants
    visaPrefixList = [
        ['4', '5', '3', '9'],
        ['4', '5', '5', '6'],
        ['4', '9', '1', '6'],
        ['4', '5', '3', '2'],
        ['4', '9', '2', '9'],
        ['4', '0', '2', '4', '0', '0', '7', '1'],
        ['4', '4', '8', '6'],
        ['4', '7', '1', '6'],
        ['4']]
    mastercardPrefixList = [
        ['5', '1'], ['5', '2'], ['5', '3'], ['5', '4'], ['5', '5']]
    amexPrefixList = [['3', '4'], ['3', '7']]

    mastercards = credit_card_number(
        mastercardPrefixList, 16, 19800 * command_object.data_size)
    visas = credit_card_number(
        visaPrefixList, 16, 19800 * command_object.data_size)
    amexes = credit_card_number(
        amexPrefixList, 15, 19800 * command_object.data_size)

    all_cards = mastercards + visas + amexes
    return all_cards


def generate_ssn():
    ssn = randomNumbers(9)
    ssn = ssn[0:3] + "-" + ssn[3:5] + "-" + ssn[5:9]
    return ssn


def http_server():
    Thread(target=serve_on_port, args=[443]).start()
    return


def randomNumbers(b):
    """
    Returns a random string/key of "b" characters in length, defaults to 5
    """
    random_number = int(''.join(random.choice(string.digits) for x in range(b))
                        ) + 10000

    if random_number < 100000:
        random_number = random_number + 100000

    return str(random_number)


def serve_on_port(port):
    if port == 443:
        cert_path = os.getcwd() + '/server.pem'
        server = ThreadingHTTPServer(("0.0.0.0", port), GetHandler)
        server.socket = ssl.wrap_socket(
            server.socket, certfile=cert_path, server_side=True)
        server.serve_forever()
    elif port == 80:
        server80 = ThreadingHTTPServer(("0.0.0.0", port), GetHandler)
        server80.serve_forever()
    return


def title_screen():
    os.system('clear')
    print "################################################################################"
    print "#                               Egress-Assess                                  #"
    print "################################################################################\n"


if __name__ == "__main__":

    title_screen()

    cli_parsed = cli_parser()

    if cli_parsed.http or cli_parsed.https:
        if cli_parsed.ssn:
            # Generate 150000 SSNs for http(s) transfer
            # This is about 1.9 megs
            post_data = ''
            for single_ssn in range(0, 81500 * cli_parsed.data_size):
                post_data += generate_ssn() + ', '
            if cli_parsed.https:
                post_url = 'https://' + cli_parsed.ip + '/ssndata.php'
            elif cli_parsed.http:
                post_url = 'http://' + cli_parsed.ip + '/ssndata.php'

        elif cli_parsed.cc:
            # Generate about 1.8 megs of different credit cards
            post_data = ''
            credit_cards = generate_credit_cards(cli_parsed)
            for card in credit_cards:
                post_data += card + ', '
            # Setup URL that data is sent to, then post it there
            if cli_parsed.https:
                post_url = 'https://' + cli_parsed.ip + '/ccdata.php'
            elif cli_parsed.http:
                post_url = 'http://' + cli_parsed.ip + '/ccdata.php'

        try:
            f = urllib2.urlopen(post_url, post_data)
            f.close()
            print "[*] File sent!!!"
        except urllib2.URLError:
            print "[*] Error: Web server may not be active on " + cli_parsed.ip
            print "[*] Error: Please check server to make sure it is active!"
            sys.exit()

    elif cli_parsed.ftp:
        ftp_client_connect(cli_parsed)

    elif cli_parsed.http_server:
        try:
            print "[*] Starting web server..."
            # bind to all interfaces
            Thread(target=serve_on_port, args=[443]).start()
            Thread(target=serve_on_port, args=[80]).start()
            print "[*] Web server is currently running"
            print "[*] Type \"killall -9 python\" to stop the web server."
        # handle keyboard interrupts
        except KeyboardInterrupt:
            print "[!] Rage quiting, and stopping the web server!"

    elif cli_parsed.ftp_server:
        ftp_server(cli_parsed)
