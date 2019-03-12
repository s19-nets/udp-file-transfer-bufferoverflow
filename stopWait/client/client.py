#! /usr/bin/env python3

import os,re
import sys,time

from socket import *
from select import select 

from clientstatemachine import ClientStateMachine
from filehelper import FileHelper

server_addr = ('localhost', 50000)

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

def idle_handler(sock, server, msg):
    global statemachine, filehelper
    # Get user input and send its action to server
    action = input("What would you like to do? GET or PUT a file? ex. GET:<filedir/filename>")
    # set our file in our filehelper object
    filehelper.setfile(action[4:])
    sock.sendto(action.encode(),server)
    statemachine.on_event({'event':'msg_send','msg':action[:3]})
    return action, server

def get_handler(sock, server, msg):
    global statemachine
    # if msg is DAT save the payload in file
    # if msg is END send BYE
    


statemachine = ClientStateMachine()

client_socket = socket(AF_INET, SOCK_DGRAM)

read_set = set([client_socket])
write_set = set()
error_set = set([client_socket])
timeout = 5

statehandler = {}
#statehandler['IdleState'] = idle_handler
statehandler['WaitState'] = wait_handler
statehandler['GetState'] = get_handler
#statehandler['PutHandler'] = put_handler

filehelper = FileHelper()

sentmsg = None
server = None
#state = 'idle'

requestfile = "foo.txt"
last_ackmsg = 0
last_msgrecv = None
# handle our idle state to get user input
sentmsg,server = statehandler[statemachine.getCurrentState()](client_socket,server_addr,None)
while True: 
    readready, writeready, error = select(read_set, write_set, error_set, timeout)

    if not readready and not writeready and not error:
        statemachine.on_event({'event':'timeout', 'msg':sentmsg})
        sentmsg,server = statehandler[statemachine.getCurrentState()](client_socket, server_addr, sentmsg)
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
        recvmsg, server = sock.recvfrom(100)
        recvmsg = recvmsg.decode()
        statemachien.on_event({'event':'msg_recv', 'msg':recvmsg})
        server, sentmsg = statehandler[statemachine.getCurrentState()](sock,server,recvmsg)

client_socket.close()
