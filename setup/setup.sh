#!/bin/bash

clear
echo "[*] Installing Egress-Assess Dependencies..."
apt-get update
apt-get -y install smbclient
echo "[*] Installing pip"
apt-get -y install pip
echo "[*] Installing scapy"
apt-get -y install python-scapy
echo "[*] Installing paramiko"
apt-get -y install python-paramiko python-crypto
echo "[*] Installing ecdsa"
pip install ecdsa
echo "[*] Installing pyasn1"
apt-get -y install python-pyasn1
echo "[*] Installing dnspython"
apt-get -y install python-dnspython
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
echo "[*] Installing cryptography v2.2.2"
pip install cryptography==2.2.2
echo "[*] Installing dnslib"
pip install dnslib
cd ../protocols/servers/serverlibs/web
clear
echo "[*] Generating SSL Certificate"
openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
echo
echo
echo "[*] Install complete!"
echo "[*] Enjoy Egress-Assess!"
