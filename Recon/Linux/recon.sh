#!/usr/bin/env bash
#
# Info grabbing collection script
#
# First parameter to running this, is the path of log file to create


echo "Linux system info " > $@
echo "" >> $@

echo "Interfaces" >> $@
echo "##############" >> $@
ifconfig -a >> $@
echo "" >> $@

echo "Mounted FS" >> $@
echo "##############" >> $@
findmnt -A >> $@
echo "" >> $@

echo "Users" >> $@
echo "##############" >> $@
awk -F':' '{print $1}' /etc/passwd >> $@
echo "" >> $@

echo "Processes" >> $@
echo "##############" >> $@
ps -ax >> $@
echo "" >> $@

echo "Interfaces (netstat)" >> $@
echo "##############" >> $@
netstat --interfaces >> $@
echo "" >> $@

echo "USB hardware" >> $@
echo "##############" >> $@
lsusb -v >> $@
echo "" >> $@

echo "Browser Credentials sql folder" >> $@
echo "##############" >> $@
ls ~/.mozilla/firefox/ >> $@
echo "" >> $@

echo "SSH" >> $@
echo "############## if nothing is printed, SSH is not running" >> $@
netstat -plan | grep ":22" >> $@
echo "" >> $@

