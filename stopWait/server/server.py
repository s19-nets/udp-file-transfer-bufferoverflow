#! /usr/bin/env python3

import os,re
import sys,time

from socket import *
from select import select

file_split = {}

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
        GET msg struct = 'GET:filename'
        PUT msg struct = 'PUT:filename' ?? 
        ACK msg struct = 'ACK:s<segment number>' '''
    global state

    msg, client_addr = sock.recvfrom(100)
    msg = msg.decode()
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
            state = 'end'
        else: 
            state = 'process_put'
    elif msg.find("ACK") == 0:
        msg = msg[5:]
        state = 'process_get'
    else: 
        print("wow")
    return (msg, client_addr)

def process_get(sock, client_addr, msg): 
    ''' Check if our data has been prepared other wise go on 
        and send data to client '''
    if msg.find("files/") == 0 and len(file_split) == 0: 
        segment = 1
        openfile = open(msg, "rb")
        data = openfile.read(100)
        while data: 
            file_split[segment] = data
            data = openfile.read(100)
            segment += 1 
        msg = 0
    next_segment = int(msg) + 1
    msg = next_segment + ":" + file_split[next_segment]
    sock.sendto(msg, client_addr)
    state = 'wait'
    return time.time()


def process_put(sock, client_addr, msg): 
    pass

def end(sock, msg): 
    pass

def wait(sock, msg): 
    pass

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(server_addr)

read_set = set()
write_set = set()
error_set = set()


state_machine = {}

state_machine['process_get'] = process_get
state_machine['process_put'] = process_put
state_machine['end'] = end
state_machine['wait'] = wait
timeout = 5

state = 'idle' 

while True: 
    readready, writeready, error = select(read_set,write_set,error_set,timeout)
    if not readready: 
        if state == 'wait' and time.time() - sent_time >= 5: 

    for sock in readready: 
        msg, client_addr = process_recvmsg(sock)
        action_time = state_machine[state](sock,client_addr, msg)
