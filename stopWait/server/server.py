#! /usr/bin/env python3
from serverstatemachine import ServerStateMachine
from filehelper import FileHelper

import os,re
import sys,time 

from socket import *
from select import select

#uncomment the line below if you want to use the proxy
server_addr = ("", 50001) 
#server_addr = ("", 50000)

def usage(): 
    print("Usage %s: [--serverport <port>]" % sys.argv[0])
    sys.exit(1)

try: 
    args = sys.argv[1:]
    while args: 
        sw = args[0]; del args[0]
        if sw == "--serverport": 
            server_addr = ("", int(args[0]))
        else: 
            print("Unexpected parameter")
            usage()
except: 
    usage()

def idle_handler(sock, client, msg): 
    ''' Rest our previous client variables and our tires '''
    global tries,filehelper

    tries = 0 
    filehelper.reset()
    print("Waiting for a client to connect...")
    return (None,)*2

def wait_handler(sock, client, msg):
    global tries
    tries += 1
    if tries == 5: 
        statemachine.on_event({'event':'err_to','msg':None})
    elif client != None and msg != None: 
        print("Attempt %d: %s"%(tries,msg))
        sock.sendto(msg.encode(), client)
    else: 
        print("Waiting for message from client")
    return (client,msg)

def get_handler(sock, client, msg): 
    global statemachine,filehelper

    if msg[:3] == "GET": 
        # set filename and split the file
        filename = "files/" + msg[4:]
        filehelper.setfile(filename)
        filehelper.splitfile()
        # set msg to 0 so that code can continue
        msg = 0
    else: 
        # set up message to just contain the segment number that was ACK
        msg = msg[5:]

    segnum = int(msg) + 1
    segment = filehelper.getsegment(segnum)
    if segment != -1: 
        segment = "DAT:" + str(segnum) + ":" + segment.decode()
    else: 
        segment = str('END') + ":" + " "
    print("Send: %s"%segment)
    sock.sendto(segment.encode(), client)
    statemachine.on_event({'event':'msg_sent','msg':msg})
    return (client,segment)

def put_handler(sock, client, msg): 
    global statemachine, filehelper
    
    if msg[:3] == "PUT": 
        fname = "files/" + msg[4:]
        if filehelper.fileexists(fname): 
            print("file already exists")
        else: 
            # just set the file name of our file helper
            # our function writetofile takes care of creating the file
            filehelper.setfile(fname)
            sendmsg = "RDY:"+fname
            sock.sendto(sendmsg.encode(), client)
            statemachine.on_event({'event':'msg_sent','msg':sendmsg})
            return (client,sendmsg)
        segnum = int(msg[1:2]) # struct of our segment msg = s<segnum>:<payload>
        payload = msg[3:]
        filehelper.writetofile(payload)
        sendmsg = "ACK:s"+segnum
        sock.sendto(sendmsg.encode(),client)
        statemachine.on_event({'event':'msg_sent','msg':sendmsg})
        return (client,sendmsg)

# TODO: add a state where if an error happens that state machine 
#       cant handle, the error state will log that error

filehelper = FileHelper()

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(server_addr)
server_socket.setblocking(False)

read_set = set([server_socket])
write_set = set()
error_set = set([server_socket])

statemachine = ServerStateMachine()
statehandler = {}
statehandler['IdleState'] = idle_handler
statehandler['WaitState'] = wait_handler
statehandler['GetState'] = get_handler 
statehandler['PutState'] = put_handler

sentmsg = None
lastclient = None

timeout = 10
tries = 0
while True: 
    readready, writeready, error = select(read_set,write_set,error_set,timeout)
    if not readready and not writeready and not error: 
        print("timeout")
        statemachine.on_event({'event':'timeout', 'msg':None})
        lastclient,sentmsg=statehandler[statemachine.getCurrentState()](server_socket,lastclient,sentmsg)
    for sock in readready: 
        tries = 0
        msg, client = sock.recvfrom(100)
        msg = msg.decode()
        statemachine.on_event({'event':'msg_recv', 'msg':msg[:3]})
        lastclient,sentmsg = statehandler[statemachine.getCurrentState()](sock,client,msg)
