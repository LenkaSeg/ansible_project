#!/bin/bash -x


echo"[webserver]" >> /etc/ansible/hosts

vagrant status | \
	awk '$2 == "running" {print $1}' | \
       	xargs -n1 -I {} sh -c "vagrant ssh {} -c 'ip -4 a show dev eth1' | \
 cut -c10-21 | sed -n '2p'" > /etc/ansible/hosts

