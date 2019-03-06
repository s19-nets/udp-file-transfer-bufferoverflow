#! /usr/bin/env python3
from serverstatemachine import ServerStateMachine

import os,re
import sys,time 

from socket import *
from select import select

#server_addr = ("", 50001) # uncomment this line when using proxy
server_addr = ("", 50000)

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
    global tries
    tries = 0 
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
    ''' Check if our data has been prepared other wise go on 
        and send data to client '''
    global statemachine,filehelper
    #print("%s %d"%(msg, len(file_split)))
    if msg[:3] == "GET": 
        # set filename and split the file
        filename = "files/" + msg[4:]
        filehelper.setfile(filename)
        filehelper.splitfile()
        # set msg to 0 so that code can continue
        msg = 0
    else: 
        msg = msg[5:]
    segnum = int(msg) + 1
    segment = filehelper.getsegment(segnum)
    print(segment)
    if segment != -1: 
        segment = str(segnum) + ":" + segment.decode()
    else: 
        # probably change the file end message to "END:<empty>"
        segment = str(-1) + ":" + " "
    print("Send: %s"%segment)
    sock.sendto(segment.encode(), client)
    statemachine.on_event({'event':'msg_sent','msg':msg})
    return (client,segment)

# TODO: put request needs to be handled 
def put_handler(sock, client_addr, msg): 
    pass


# TODO: add a state where if an error happens that state machine 
#       cant handle, the error state will log that error


class FileHelper(object):
    def __init__(self):
        self.filename = None
        self.splitedfile = {}
        
    def setfile(self,filename):
        self.filename = filename

    def splitfile(self): 
        f = open(self.filename, "rb")
        index = 1
        data = f.read(100)
        while data: 
            self.splitedfile[index] = data
            data = f.read(100)
            index += 1

    def getsegment(self, segnum): 
        return self.splitedfile[segnum] if segnum in self.splitedfile else -1

filehelper = FileHelper()

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(server_addr)
server_socket.setblocking(False)

read_set = set([server_socket])
write_set = set()
error_set = set([server_socket])

statemachine = ServerStateMachine()
''' TODO: handler funcs for all other states '''
statehandler = {}
statehandler['IdleState'] = idle_handler
statehandler['WaitState'] = wait_handler
statehandler['GetState'] = get_handler 

sentmsg = None
lastclient = None

timeout = 10
tries = 0
while True: 
    readready, writeready, error = select(read_set,write_set,error_set,timeout)
    if not readready and not writeready and not error: 
        print("timeout")
        statemachine.on_event({'event':'timeout', 'msg':None})
        lastclient,sentmsg=statehandler[statemachine.state.__str__()](server_socket,lastclient,sentmsg)
        #counter += 1
        #if state == 'idle': 
            #counter = 0
        #if state == 'wait': 
            #sock.sendto(sent_msg.encode(), client)
        #if counter == 10: 
            #print("Connection lost")
    for sock in readready: 
        msg, client = sock.recvfrom(100)
        msg = msg.decode()
        statemachine.on_event({'event':'msg_recv', 'msg':msg[:3]})
        lastclient,sentmsg = statehandler[statemachine.state.__str__()](sock,client,msg)
