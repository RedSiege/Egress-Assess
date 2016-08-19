#Customize the certificate below if you wish. Otherwise this file is good to go.
#See ./setup/Dockerfile for instructions to build a docker image
#!/bin/bash

clear
echo "[*] Installing Egress-Assess Dependencies..."
apt-get install -y smbclient
echo "[*] Installing scapy"
apt-get install -y python-scapy
echo "[*] Installing paramiko"
apt-get install -y python-paramiko python-crypto
echo "[*] Installing ecdsa"
pip install ecdsa
echo "[*] Installing pyasn1"
apt-get install -y python-pyasn1
echo "[*] Installing dnspython"
apt-get install -y python-dnspython
echo "[*] Installing impacket"
wget https://pypi.python.org/packages/source/i/impacket/impacket-0.9.13.tar.gz
tar -xvf impacket-0.9.13.tar.gz
cd impacket-0.9.13
python setup.py install
cd ..
rm -rf impacket-0.9.13
echo "[*] Installing pyftpdlib..."
git clone https://github.com/giampaolo/pyftpdlib.git
cd pyftpdlib
python setup.py install
cd ..
rm -rf pyftpdlib
cd /Egress-Assess/protocols/servers/serverlibs/web
clear
echo "[*] Generating SSL Certificate"
#Change the certificate information in the below line if you wish
openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes -subj "/C=US/ST=Texas/L=Huston/O=Another Network/OU=IT Department/CN=www.change.org"
echo
echo
echo "[*] Install complete!"
echo "[*] Enjoy Egress-Assess!"
