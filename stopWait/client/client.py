#! /usr/bin/env python3

import os,re
import sys,time

from socket import *
from select import select 

from clientstatemachine import ClientStateMachine

server_addr = ('localhost', 50000)

def getactionfromuser():
    action = input("What would you like to do?GET or PUT a file? ex. GET <filedir/filename>")
    return action

#def process_recvmsg(sock):
#    global state
#    msg, sender_addr = sock.recvfrom(102)
#    msg = msg.decode()
#    print("recived: %s"%msg)
#    if state == 'wait': 
#        if msg[:3] != "ACK":
#           return process_get(sock, msg, sender_addr)
#    return None
#
#def process_get(sock, msg, sender_addr): 
#    global state, requestfile, last_ackmsg
#    openfile = open("files/"+requestfile, "a")
#    msg_split = msg.split(":")
#    if msg_split[0] != "END":
#        openfile.write(msg_split[2])
#        if last_ackmsg == int(msg_split[1]):
#            return
#        msgto_send = "ACK:s"+msg_split[1]
#        sock.sendto(msgto_send.encode(),sender_addr)
#        last_ackmsg = int(msg_split[1])
#        state = 'wait'
#    else: 
#        msgto_send = "BYE:Thank you"
#        sock.sendto(msgto_send.encode(), sender_addr)
#        state = 'end'
#    return msgto_send
statemachine = ClientStateMachine()
action = getactionfromuser()

client_socket = socket(AF_INET, SOCK_DGRAM)

read_set = set([client_socket])
write_set = set()
error_set = set([client_socket])
timeout = 5


#state = 'idle'

requestfile = "foo.txt"
last_ackmsg = 0
last_msgrecv = None
getsent = False
while True: 
    readready, writeready, error = select(read_set, write_set, error_set, timeout)

    if not readready and not writeready and not error: 
        #if state == 'idle' and not getsent:
        #    open("files/"+requestfile, "w+") # create file
        #    msgto_send = "GET:" + requestfile
        #    print("Send: %s"%msgto_send)
        #    client_socket.sendto(msgto_send.encode(), server_addr)
        #    getsent = True
        #    state = 'wait'
        #if state == 'end':
        #    break
        #if state == 'wait' and last_msgrecv != None:
        #    client_socket.sendto(last_msgrecv.encode(), server_addr)

    for sock in readready: 
        #last_msgrecv = process_recvmsg(sock)

client_socket.close()
