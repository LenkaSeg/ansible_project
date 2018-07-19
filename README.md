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
- I run ```ip -4 a show dev eth1``` to retrieve the IP from each VM, but the output is a little 
longer than just IP. 
To get just the IP I ran:

```vagrant status | awk '$2 == "running" {print $1}'| \```
 ```xargs -n1 -I{} sh -c "vagrant ssh {} -c 'ip -4 a show dev eth0' | \```
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


