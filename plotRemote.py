#!/usr/bin/python

import os
import matplotlib

#This must be imported before importing pylab

#This script detects if a session is being run remotely:
#if remote - save figure to directory BASEDIR
#if local - plot it

#use plotRemote.prshow() instead of pylab.show()

from lazy import REMOTESESSION_BASEDIR

try:
    os.environ['SSH_CLIENT']
except KeyError:
    #Local connection
    REMOTESESSION = False
else:
    REMOTESESSION = True
    import matplotlib
    matplotlib.use("Agg")

def prshow(fname="lazy.png"):
    if REMOTESESSION:
        matplotlib.pyplot.savefig(REMOTESESSION_BASEDIR + fname)
        print "Wrote file %s"%(REMOTESESSION_BASEDIR + fname)
    else:
        matplotlib.pyplot.show()

#Example special case for a specific server
#import socket
#if socket.gethostname()=="some_server_name":
#    REMOTESESSION = False
#    import matplotlib
#    matplotlib.use('WX')

