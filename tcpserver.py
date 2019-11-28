#! /usr/bin/python

# FileName: tcpserver.py
# Author: Joe Gumke
# Asmt Number: 6
# Date: 2/2/2010
# Class: CSIS 440
#$Id: tcpserver.py,v 1.1 2010/03/05 20:02:18 joe Exp $

# Import Modules
import socket
from sys import *
import select
import string
import time

# Start Definition of Class
class IrcServe:
    # Class Constructor
    def __init__(self,PORT):
        # Create socket and bind to itself with specified port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("",PORT))
        self.sock.listen(20)    
        self.connList=list()
        self.clientList=[]
        self.asciiMesgList=[32,48,49,50,51,52,53,54,55,56,57,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,
82,83,84,85,86,87,88,89,90,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,
112,113,114,115,116,117,118,119,120,121,122]
        self.asciiNickList=[48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,
75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,
102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122]
        # Create read list for select to watch
        self.rlist = [self.sock,stdin]
        self.wlist = []
        print "Listening on Port:",PORT,"...."

    # Function for initial connections
    def select_loop(self):
        try: 
            self.inputready,self.outputready,garbage2 = select.select(self.rlist,self.wlist,[],0)
        except select.error, e: print "Select Error:",self.error_msg(e)
        except socket.error, e: print "Socket Error:",self.error_msg(e) 
        self.loop()

    # Function for looping, handles a large part of the processing
    def loop(self):
        for i in self.inputready:
            if i == self.sock: 
                self.accept_conn()

            elif i == stdin:
                try:
                    for r in self.connList:
                            r[0].send("Server Closing Down....")
                            r[0].close()
                    self.sock.close()
                except socket.error:
                    self.sock.close()

            else:
                try:
                    # Attempt to read from socket 
                    data = i.recv(256)
                    if data:
                        # Start processing Messages that get send back and forth for valid characters
                        self.joeWord = ""
                        for u in data:
                            tempWord = ord(u)
                            if tempWord in self.asciiMesgList:
                                u = ""
                                try:
                                    tempWord = chr(u)
                                except:
                                    tempWord = chr(tempWord)
                            else:
                                if tempWord not in self.asciiMesgList:
                                    u = ""
                                    try:
                                        tempWord = chr(u)
                                        tempWord = ""
                                    except:
                                        tempWord = chr(tempWord)
                                        tempWord = ""
                            self.joeWord = self.joeWord +tempWord

                        for s in self.connList:
                            if s[0]==i:
                                msg = "(" + s[1] + ")" + "," + "[" +s[2] +"]"+"Nick:"+s[3] + " >> " + self.joeWord + "\n"
                                print "sendn data: ",msg
                        for x in self.wlist:
                            if x != i :
                                x.send(msg)

                    else:
                        for t in self.connList:
                             if i == t[0]:
                                 diemsg = t[3] +str(" Has left the Chat Room \n")
                                 self.clientList.remove(t[3])
                                 self.connList.remove(t)
                                 for h in self.connList:  
                                     h[0].send(diemsg)   
                        for m in self.wlist:   
                             if m == i:                              
                                self.rlist.remove(m)
                                self.wlist.remove(m)                      
                                                
                except socket.error, e:
                    try:
                        self.rlist.remove(i)
                        self.wlist.remove(i)
                    except ValueError:
                        print "oops LINE 131"

    # Function for accepting connections
    def accept_conn(self):
        conn, addr = self.sock.accept()
        # Format IP and Port 
        ipAddr = addr[:1]
        ipAddr = ' '.join(ipAddr)
        self.tempIpAddr = ipAddr  
        portAddr = addr[1:]
        portAddr = str(portAddr)
        portAddr = portAddr[1:6]
        self.tempConn = conn
        
        # Client Connection Code    
        if len(self.rlist[2:]) <= 20:
                if self.tempConn not in self.connList:
                    self.rlist.append(conn)
                    self.wlist.append(conn)

                    #print "self.connList [0]:",self.connList[0]
                    self.tempConn.send("Enter a NickName or Connection Will Close...\n")
                    try:
                        # Give client 3 Seconds to respond, else he'll get kicked
                        self.tempConn.settimeout(3)
                        self.recvNick = self.tempConn.recv(8)  
                        self.Nick= ""  
                        tempWord = ""
                        for u in self.recvNick:
                            tempWord = ord(u)
                            if tempWord in self.asciiNickList:
                                u = ""
                                try:
                                    tempWord = chr(u)
                                except:
                                    tempWord = chr(tempWord)
                            else:
                                if tempWord not in self.asciiNickList:
                                    u = ""
                                    try:
                                        tempWord = chr(u)
                                        tempWord = ""
                                    except:
                                        tempWord = chr(tempWord)
                                        tempWord = ""
                            self.Nick = self.Nick +tempWord
                        self.Nick = self.Nick.rstrip('\n')
                        self.Nick = self.Nick.rstrip('\r')

                        # Error Handle Clients that take too long for Nickname and Check for Duplicate Nicknames
                        tempVar = 0
                        for self.y in self.connList:
                            if self.Nick == self.y[3] and self.Nick == "" and self.Nick == " " and self.Nick == "   ":
                                #print "SELF.NICK:",self.Nick
                                tempVar = 1

                        # If username picked is taken....kick user and tell him to try again
                        if tempVar == 1:
                            try:
                                self.tempConn.send("NickName already taken.....Connection Will close... Try Again Later..\n") 
                            except socket.error:
                                print "oops"
                            self.rlist.remove(conn)
                            self.wlist.remove(conn)
                            self.clientList.remove(self.y[3])
                            self.connList.remove(self.y)
                            self.tempConn.close()

                        # If username doesn't exist, add user and go on with life
                        elif tempVar ==0:
                            self.connList.append([conn,ipAddr,portAddr,self.Nick])       
                            self.tempConn.send("Welcome to Joe's IRC..."+'\n')
                            self.clientList.append(self.Nick)
                            for i in self.connList:
                                i[0].send(self.Nick+" has now joined the chat...\n")
                    # Error Handling for socket timeouts
                    except socket.timeout:
                        try:
                            self.tempConn.send("No NickName Entered...Connection Will Close, Try Again \n")
                            self.rlist.remove(conn)
                            self.wlist.remove(conn)
                            #if self.Nick:
                            #    self.clientList.remove(self.Nick)
                            self.tempConn.close()
                        except socket.error:
                            print "Tried to Kill, But No Cigar"
                    
        # If statement to handle client list that goes over 20 members
        elif len(self.rlist) >= 21:
           self.tempConn.send("Sorry the ChatRoom is Currently Full...Try Again Later....\n")
           self.tempConn.close()

    # Error Reporting Function
    def error_msg(self,e):
        print e
        exit(1)

if __name__ == '__main__':

    # Set argument count statically to 2, else program will exit & complain
    argc = len(argv)
    if argc != 2:
        print"Proper Usage: ./tcpserver.sh <PORT>"    
        exit(1)

    # Set Port to User specified
    PORT = int(argv[1])

    # Create instance of Class for method usage
    server = IrcServe(PORT)
    running = 1
    while running:
        server.select_loop()

    server.sock.close()

