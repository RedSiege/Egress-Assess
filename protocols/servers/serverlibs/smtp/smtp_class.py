# Code from http://pymotw.com/2/smtpd/

import smtpd
import time
from common import helpers


class CustomSMTPServer(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        print 'Receiving message from:', peer
        print 'Message addressed from:', mailfrom
        print 'Message addressed to  :', rcpttos
        print 'Message length        :', len(data)

        loot_directory = helpers.ea_path() + '/data'

        current_date = time.strftime("%m/%d/%Y")
        current_time = time.strftime("%H:%M:%S")
        file_name = current_date.replace("/", "") +\
            "_" + current_time.replace(":", "") + "email_data.txt"

        with open(loot_directory + "/" + file_name, 'w') as email_file:
            email_file.write(data)

        return
