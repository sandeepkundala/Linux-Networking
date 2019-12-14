FROM ubuntu:16.04
  
MAINTAINER Team30

RUN apt-get update && apt-get install -y openssh-server
RUN mkdir -p ~/.ssh && echo "Host *" > ~/.ssh/config && echo " StrictHostKeyChecking no" >> ~/.ssh/config 
RUN chmod 400 ~/.ssh/config
RUN mkdir /var/run/sshd
COPY /home/ece792/.ssh/authorized_keys /root/.ssh/authorized_keys
RUN chmod 700 /root/.ssh/authorized_keys
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN echo "root:1234" | chpasswd

RUN apt-get update
RUN apt-get -y --force-yes install iproute2
RUN apt-get -y --force-yes install telnet
RUN apt-get -y --force-yes install openssh-server
RUN apt-get -y --force-yes install iptables
RUN apt-get -y --force-yes install iputils-ping
RUN apt-get -y --force-yes install traceroute
RUN apt-get -y --force-yes install tcpdump
RUN apt-get -y --force-yes install iperf
RUN apt-get -y --force-yes install vim
RUN apt-get -y --force-yes install python
RUN apt-get -y --force-yes install python-pip
RUN apt-get -y --force-yes install cron
RUN pip install --upgrade pip
RUN apt-get -y --force-yes install python-pexpect
RUN pip install paramiko
COPY crontab /etc/cron.d/cool-task
RUN chmod 0644 /etc/cron.d/cool-task
RUN service cron start
RUN apt-get -y --force-yes install python3
RUN apt-get -y --force-yes install python3-pip
RUN pip3 install --upgrade pip
RUN apt-get -y --force-yes install python3-pexpect
RUN pip3 install paramiko
RUN apt-get -y --force-yes install nano

ENTRYPOINT service ssh restart

CMD    ["/usr/sbin/sshd", "-D"]

