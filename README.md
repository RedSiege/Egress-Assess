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

Blog posts are available here: 

* https://www.christophertruncer.com/egress-assess-testing-egress-data-detection-capabilities/
* https://www.christophertruncer.com/egress-assess-action-via-powershell/

Typical use case for Egress-Assess is to copy this tool in two locations.  One location will act as the server, the other will act as the client.  Egress-Assess can send data over FTP, HTTP, and HTTPS.

To extract data over FTP, you would first start Egress-Assess’s FTP server by selecting “--server ftp” and providing a username and password to use:

./Egress-Assess.py --server ftp --username testuser --password pass123

Now, to have the client connect and send data to the ftp server, you could run...

./Egress-Assess.py --client ftp --username testuser --password pass123 --ip 192.168.63.149 --datatype ssn

Also, you can setup Egress-Assess to act as a web server by running....

./Egress-Assess.py --server https

Then, to send data to the FTP server, and to specifically send 15 megs of credit card data, run the following command...

./Egress-Assess.py --client https --data-size 15 --ip 192.168.63.149 --datatype cc
