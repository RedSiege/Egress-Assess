#All client protocols work with Docker Image. Server Protocols FTP and ICMP are not currently functional.
#Build this docker file with the following command
#$cd ./setup
#$docker build -t egressassess .
#You can also just pull it from Docker hub
#docker pull piesecurity/egress-assess
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
#Example Client Execution
#docker run -it piesecurity/egress-assess
#Example Server Execution- This requires all of the port mappings and location of your loots folder
#Slight changes in port incase these are already in use
#loots can be any local folder you want
#docker run -it -p 25:25 -p 20-21:20-21 -p 60000-60100:60000-60100 -p 80:80 -p 445:445 -p 53:53/udp -p 444:443 -p 23:22 -v /home/ubuntu/loots:/Egress-Assess/data/ piesecurity/egress-assess
#Special note for running the ICMP Server in Docker: Add the below iptables rule after the docker container is running
#iptables -t nat -A PREROUTING -p ICMP -i <internet_interface> -j DNAT --to-destination <dockerContainerIP>
#You can find the <dockerContainerIP> through the docker inpsect command, or just look at the rest of your iptables rules under the DOCKER chain
