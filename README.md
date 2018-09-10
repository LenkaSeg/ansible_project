# TASK
[TASK in Trello](https://trello.com/b/fgyo48m6/lenkas-tasks "Task in Trello")

## Create a Vagrantfile that creates 4 VMs to be used for ansible tasks
- box in vagrant is like image
- setting the memory has to be under provider, not define
- put end everywhere
- adding ssh keys to all vm's in Vagrantfile with config.vm.provision
- ssh-ing to each vm's to check if the keys are there in 
.ssh/authorized_keys, and they are!

## Use 'vagrant ssh' to retrieve the IP address of the 'eth0' device ("ip -4 a show dev eth0" ) 
Bonus points if you make a bash script that does it for each machine and prints them all.

- by default Vagrant creates interface which is shared. This was the reason all VMs had the same 
IP address. If I want to have each VM with specific address, I have to use PRIVATE_NETWORK. 
- now the device is not eth0, but eth1
- I ssh-ed to each VM and ran ```ip -4 a show dev eth1``` to see the IP from each VM, but 
the output is a little longer than just IP. 
To collect all IPs at once without manually entering each VM and to get just the IP I ran:

```vagrant status | awk '$2 == "running" {print $1}'|```
 ```xargs -n1 -I{} sh -c "vagrant ssh {} -c 'ip -4 a show dev eth0' |```
 ```cut -c10-21 | sed -n '2p'" > ips```

* vagrant status shows all the VMs
* awk runs whichever command on each line, $1 are positions
* that thing after xargs I found on stackoverflow without any further explanation, so I don't 
know exactly what it does, but it works for me
* -c "" is the command a want to be ran - to ssh to vagrant, grab the IP message, cut it into 
columns and cut out extra characters, pick the middle column with sed and write it down into a 
file called ips
* the result is a file called ips with 4 IP addresses

- Now when I tested that this megacommand works, I wanted to create a bash script from it. I 
named it retrieve_IP.sh.
- Permissions: to make it runable, it's necessary to change permissions like this:

```ls -l``` 

```chmod u+x retrieve_IP.sh```

- I ran it:

```./retrieve_IP.sh```

 and there in the same directory appears a new file called ips with all 4 IP 
addresses.
It works! 


## Install ansible and create an ansible static inventory file so that the ansible playbook 
targets the aforecreated VMs

```sudo pacman -S ansible```

- inventory file can be Ini-like or Yaml-like. I used Ini version, named it hosts, without file 
extension
```sudo nano /etc/ansible/hosts```

## Make sure you have [ansible config](https://docs.ansible.com/ansible/latest/installation_guide/intro_configuration.html)

- ```ansible.cfg``` is in ```/etc/ansible```


## Place 3 VMs on the webserver group and 1 VM on the loadbalancer group
- in a way so that the ansible playbook targets the VMs - using their IPs
- NOTE - I should add it to the shell script, so I don't have to copy it manually


## Set up directory structure
- directory playbooks, inside I created file install.yml
- roles, npk for all servers, web for webservers, haproxy for loadbalancers
- roles directory and inside directories ntp, haproxy and web

## NTP role
- NTP stands for Network Time Protocol. It is of the utmost importance that your servers run with 
the same time. In case there are issues, you'll be able to read the logs of your different 
servers and the time of the events will match. Otherwise it would be very hard to establish a 
timeline.

This role will set NTP up and make sure that its service is running 

- I followed this [guide](https://www.hugeserver.com/kb/config-time-date-centos-7-ntp/)
- and it is necessary to put the commands into main.yml file, readable by ansible
- apparently there are modules for this, which can be found in ansible documentation
- I used modules: package (for ntp install), timezone (for setting timezone) and systemd (for 
enabling and starting ntpd service)
- ntpd stands for network time protocol daemon
 
## Code a flask app that replies with its hostname

- created directory echoflask with app.py file
- using the os module checked of there is an environment variable called REPLY_HOSTNAME - using 
os.environ.get('REPLY_HOSTNAME')
- if there is, return it, if not, return hostname using socket module: socket.gethostname()
- installed package python-flask
- run python app.py
- It works

## Containerize the 'echoflask' app

- Dockerfile created in echoflask
- creating user Lenka and switching to it

```
RUN useradd -ms /bin/bash lenka

USER lenka
```

- label added
- ENV [REPLY_HOSTNAME] set to unset (but I'm not sure if I understand what it's supposed to do)
- ENTRYPOINT set to run 'echoflask':

```
ENTRYPOINT ["python","app.py"]
```

- image built

```
docker build -t lenkaseg/echoflask .
```

- run

```
docker run -p 11000:11000 --name echoflask lenkaseg/echoflask
```

- dockerhub

``` 
docker login --username=lenkaseg
docker push lenkaseg/echoflask
``` 
