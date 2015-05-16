#!/bin/bash

clear
echo "[*] Installing Egress-Assess Dependencies..."
apt-get install smbclient
echo "[*] Installing pyftpdlib..."
git clone https://github.com/giampaolo/pyftpdlib.git
cd pyftpdlib
python setup.py install
cd ..
rm -rf pyftpdlib
cd ../protocols/servers/serverlibs/web
clear
echo "[*] Generating SSL Certificate"
openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
echo
echo
echo "[*] Install complete!"
echo "[*] Enjoy Egress-Assess!"
