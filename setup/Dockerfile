#All client protocols work with Docker Image. Server Protocols FTP and ICMP are not currently functional.
#Build this docker file with the following command
#$cd ./setup
#$docker build -t egressassess .
FROM ubuntu
MAINTAINER piesecurity <admin@pie-secure.org>
RUN apt-get update && \
#python-pip is just too big, but I don't think it is required right now
apt-get install tcpdump git wget -y  && \
git clone https://github.com/ChrisTruncer/Egress-Assess.git
ADD setup-docker.sh /Egress-Assess/setup/setup-docker.sh
RUN chmod +x /Egress-Assess/setup/setup-docker.sh
RUN bash -c "cd /Egress-Assess && ./setup/setup-docker.sh"
EXPOSE 80 443 53/udp 25 21 20 445
ENTRYPOINT bash -c "cd /Egress-Assess && ./Egress-Assess.py --list-servers && ./Egress-Assess.py -h && bash" 
#Example Server Execution- Slight changes in port incase these are inuse
#Loots can be any local folder you want
#docker run -it -p 25:25 -p 20:20 -p 21:21 -p 80:80 -p 445:445 -p 53:53/udp -p 444:443 -p 23:22 -v /home/ubuntu/Egress-Assess-Docker/loots:/Egress-Assess/data/ piesecurity/egressasess 
