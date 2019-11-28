#! /usr/bin/python

# FileName: ircclient.sh
# Author: Joe Gumke
# Asmt Number: 6
# Date: 3/2/2010
# Class: CSIS 440
#$Id: tcpclient.sh,v 1.3 2010/03/10 15:11:07 joe Exp $

import curses
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

pad = curses.initscr()
pad.idlok(True)
shell = curses.def_shell_mode()
pad.clear()
pad.refresh()

pad = curses.newwin(0,0)

for l in range(curses.LINES - 1):
    for c in range(curses.COLS):
        pad.addstr(l, c, '*')
        pad.refresh()
        
win1 = curses.newwin(curses.LINES -8, curses.COLS - 6, 1, 3)
win1.clear()
win1.refresh()
win1.scrollok(True)

win2 = curses.newwin(4, curses.COLS - 6, curses.LINES - 5, 3)
win2.clear()
win2.refresh()

win3 = curses.newwin(curses.LINES, curses.COLS - 6, curses.COLS-9, 3)
win3.clear()
win3.refresh()

curses.echo()
rlist = [sock,stdin]
while 1:
    win2.clear()
    sendData = win2.addstr(0, 0, 'Enter: >> ')
    try: 
        inputready,garbage1,garbage2 = select.select(rlist,[],[],0)
    except select.error, e: print "Select Error:",error_msg(e)
    except socket.error, e: print "Socket Error:",error_msg(e) 

    for i in inputready:
        if i == sock:
            recieve = i.recv(256)
            win1.addstr(recieve)
            win1.refresh()
        
        else:
            keybuf = win2.getstr()
            keybuf = keybuf #+ '\n'
            sock.send(keybuf)

sleep(10)
