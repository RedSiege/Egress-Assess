Egress-Assess
=============

Egress-Assess is a tool used to test egress data detection capabilities.

Setup
=====

To setup, run the included setup script, or perform the following:

1.  Install pyftpdlib
2.  Generate a server certificate and store it as "server.pem" on the same level as Egress-Assess.  This can be done with the following command:

"openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes"


Usage
=====

Blog post is available here: 

Typical use case for Egress-Assess is to copy this tool in two locations.  One location will act as the server, the other will act as the client.  Egress-Assess can send data over FTP, HTTP, and HTTPS.

To extract data over FTP, you would first start Egress-Assess’s FTP server by selecting “–ftp-server” and providing a username and password to use:

./Egress-Assess.py –ftp-server –username testuser –password pass123

Now, to have the client connect and send data to the ftp server, you could run...

./Egress-Assess.py --ftp --username testuser --password pass123 --ip 192.168.63.149 --ssn


Also, you can setup Egress-Assess to act as a web server by running....

./Egress-Assess.py --http-server

Then, to send data to the FTP server, and to specifically send 15 megs of credit card data, run the following command...

./Egress-Assess.py –http –data-size 15 –ip 192.168.63.149 –cc


Upcoming Changes
================

1.  Make Egress-Assess modular so users can easily extend the tool to support additional frameworks and data types.
