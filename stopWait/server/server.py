#! /usr/bin/env python3

import os,re
import sys,time 
from serverstatemachine import ServerStateMachine

from socket import *
from select import select


file_split = {}

#server_addr = ("", 50001) # uncomment this line when using proxy
server_addr = ("", 50000)

state = 'idle'

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

def process_recvmsg(sock): 
    ''' Process messages:
        GET msg struct = 'GET:filename.txt'
        PUT msg struct = 'PUT:filename' ?? 
        ACK msg struct = 'ACK:s<segment number>' '''
    global state
    msg, client_addr = sock.recvfrom(100)
    msg = msg.decode()
    print("recived: %s"%msg)
    if msg.find("GET") == 0: 
        msg = "files/" + msg[4:]
        if os.path.isfile(msg): 
            state = 'process_get'
        else:
            msg = "file not found"
            state = 'end'
    elif msg.find("PUT") == 0: 
        msg = "files/"+ msg[4:]
        if os.path.isfile(msg): 
            msg = "File exist already"
            state = 'end'
        else: 
            state = 'process_put'
    elif msg.find("ACK") == 0:
        msg = msg[5:]
        state = 'process_get'
    elif msg.find("Thank") == 0: 
        state = 'idle'
        # reset file_split since we have completed this request
        file_split = {}
    else: 
        print("Something wrong happened")
    return (msg, client_addr)

def process_get(sock, client_addr, msg): 
    ''' Check if our data has been prepared other wise go on 
        and send data to client '''
    global state,filehelper
    print("%s %d"%(msg, len(file_split)))
    if msg.find("files/") == 0 and len(file_split) == 0: 
        # set filename and split the file
        filehelper.setfile(msg)
        filehelper.splitfile()
        # set msg to 0 so that code can continue
        msg = 0
    segnum = segment = int(msg) + 1
    segment = filehelper.getsegment(segment)
    print(segment)
    if segment != -1: 
        msg = str(segnum) + ":" + segment.decode()
    else: 
        msg = str(-1) + ":" + " "
    print("Send: %s"%msg)
    sock.sendto(msg.encode(), client_addr)
    state = 'wait'
    return msg

def process_put(sock, client_addr, msg): 
    global state
    if msg.find("files/") == 0 and not os.path.isfile(msg): 
        # first create our file
        open(msg, "w+")


# Log that something went wrong
def end(sock, msg): 
    pass


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

#state_machine = {}
#state_machine['process_get'] = process_get
#state_machine['process_put'] = process_put

statemachine = ServerStateMachine()
statehandler = {}

timeout = 10

counter = 0
while True: 
    readready, writeready, error = select(read_set,write_set,error_set,timeout)
    if not readready and not writeready and not error: 
        print("timeout")
        statemachine.on_event({'event':'timeout', 'msg':None})
        #counter += 1
        #if state == 'idle': 
            #counter = 0
        #if state == 'wait': 
            #sock.sendto(sent_msg.encode(), client)
        #if counter == 10: 
            #print("Connection lost")
    for sock in readready: 
        msg, client = sock.recvfrom(100)
        statemachine.on_event({'event':'msg_recv', 'msg':msg[:3]})
        #msg, client= process_recvmsg(sock) 
        #if state != 'idle': 
            #sent_msg = state_machine[state](sock,client, msg)
