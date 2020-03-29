Requirements

1. 'netfilterqueue' module must be installed on python and its dependencies
	*. On debian or Ubuntu, install these files iwht:
		apt-get install build-essential python-dev libnetfilter-queue-dev
	*. then install netfilterqueue
		pip install NetfilterQueue
2. 'scapy' module
	*. Install scapy with this command:
		pip install scapy
3. you must be in the same network or subnet as target to run this script

4. If you get error of missing module, kindly install that module through pip command


Usage Direction

1. For capturing the victim's packets in our machine, run this command 
	iptables -I FORWARD -j NFQUEUE --queue-num 0
	
2. Port forwarding must be enabled. It can be enabled with this command on linux debian
	echo 1 > /proc/sys/net/ipv4/ip_forward

3. Become the man in the middle by running the arp_spoofing.py script located in 'ARP Spoofing' folder against the target.

4. Run the specific python file.
	

*. Guidence for net_cut.py script
	It cuts the victim's internet connection by droping all the packets arriving at script running machine.


*. Guidence for dns_spoofer.py script - 
	It spoofs a target's dns request and thus can be redirected to some other Ip.
	This script runs with command line arguments
	-h : for help
	-n : URL of website to be spoofed of
	-i : Ip to be redirected to after dns resolution

