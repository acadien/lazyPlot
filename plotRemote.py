#!/usr/bin/python

#Set this variable to select a directory to spit out plots in. Handy when used in conjunction with Dropbox.
REMOTESESSION_BASEDIR=None

import os
import matplotlib

#This must be imported before importing pylab

#This script detects if a session is being run remotely:
#if remote - save figure to directory BASEDIR
#if local - plot it

#use plotRemote.prshow() instead of pylab.show()



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
    if REMOTESESSION_BASEDIR=None:
        REMOTESESSION_BASEDIR="./"
    
    if REMOTESESSION:
        matplotlib.pyplot.savefig(REMOTESESSION_BASEDIR + fname)
        print "Wrote file %s"%(REMOTESESSION_BASEDIR + fname)
    else:
        matplotlib.pyplot.show()

REMOTESESSION_BASEDIR=REMOTESESSION_BASEDIR.rstrip("/")+"/"

#Example special case for a specific server
#import socket
#if socket.gethostname()=="some_server_name":
#    REMOTESESSION = False
#    import matplotlib
#    matplotlib.use('WX')

