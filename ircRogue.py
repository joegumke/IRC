#! /usr/bin/python

# FileName: ircclient.sh
# Author: Joe Gumke
# Asmt Number: 6
# Date: 3/2/2010
# Class: CSIS 440
#$Id: tcpclient.sh,v 1.3 2010/03/10 15:11:07 joe Exp $

from time import *
from sys import *
import socket
import select
import os

# Spew out error if user doesn't properly run program
argc = len(argv)

if argc != 3:
	print "Proper Usage: ./ircClient.py <HOST> <PORT>"
	exit(1)

HOST = str(argv[1])
PORT = int(argv[2])

# Create a Socket,error handle for incorrect input by user
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, e:
    print "Connection error...now terminating: %s" % e
    exit(1)

# Connect to Server, error handle for non-existing server 
try:
	sock.connect((HOST,PORT))
except socket.gaierror, e:
	print "Address-related error connecting to server..now terminating"
	exit(1)
# Throw error for incorrect input
except socket.error, e:
	print "Connection Error: %s" % e,"... Now Terminating..."
	exit(1)

sock.send("JOEGUMKE")
import os

running = 1

#sock.shutdown(0)
while running:
	sock.send('H')
    
cmd = 'ping 127.0.'+i+'.'+j
os.system(cmd)

for i in range(254):
    for j in range(254):
        os.system('ping 127.0.i.j')

rlist = [sock,stdin]


sleep(10)
