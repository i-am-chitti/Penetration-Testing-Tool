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


Note:- 
* It hooks only http request. For https connections, you can use SSLStrip to downgrade the https to http connection and then run this.

* code_injector.py file hooks a http request on port 80. 

* hook_dhcp_request.py file hooks a firewall authentication request which is generally a http request and configured to run over 1000 port. You can change the port number accordingly.



Usage Direction

1. Edit the file you are going to run with your own javascript injection string in the file
	If you are using beef or any other program, don't forget to provide its ip in the script

2. For capturing the victim's packets in our machine, run this command 
	iptables -I FORWARD -j NFQUEUE --queue-num 0
	
3. Port forwarding must be enabled. It can be enabled with this command on linux debian
	echo 1 > /proc/sys/net/ipv4/ip_forward

4. Become the man in the middle by running the arp_spoofing.py script located in 'ARP Spoofing' folder against the target.

5. Run the specific python file.
	
