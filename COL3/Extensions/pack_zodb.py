#!/usr/bin/python
import sys, urllib
if len(sys.argv)< 3:
  print "\nUsage: <zopectl> pack_zodb <host> <days-of-history>"
  print "  e.g., bin/instance1 run src/Products/COL3/Extensions/pack_zodb.py http://col3dev.tnc.org 10"
else:
    host = sys.argv[1]
    days = sys.argv[2]
    url = "%s/Control_Panel/Database/manage_pack?days:float=%s" % \
          (host, days)
    try: 
        f = urllib.urlopen(url).read()
        print "Successfully packed ZODB on host %s" % host    
    except IOError:
        print "Cannot open URL %s, aborting" % url
        print "ZODB pack failed on host %s" % host