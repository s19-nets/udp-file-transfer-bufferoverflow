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
    elif msg == "Thank you, Goodbye": 
        state = 'idle'
    else: 
        print("Something wrong happened")
    return (msg, client_addr)

def process_get(sock, client_addr, msg): 
    ''' Check if our data has been prepared other wise go on 
        and send data to client '''
    global state
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
    if next_segment in file_split: 
        msg = str(next_segment) + ":" + str(file_split[next_segment], "UTF-8")
    else: 
        msg = str(-1) + ":" + " "
    print("Send: %s"%msg)
    sock.sendto(msg.encode(), client_addr)
    state = 'wait'
    return msg

def process_put(sock, client_addr, msg): 
    pass

# Log that something went wrong
def end(sock, msg): 
    pass

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(server_addr)
server_socket.setblocking(False)

read_set = set([server_socket])
write_set = set()
error_set = set([server_socket])


state_machine = {}
state_machine['process_get'] = process_get
state_machine['process_put'] = process_put

timeout = 10

counter = 0
while True: 
    readready, writeready, error = select(read_set,write_set,error_set,timeout)
    if not readready and not writeready and not error:
        print("timeout")
        counter += 1
        if state == 'idle': 
            counter = 0
        if state == 'wait': 
            sock.sendto(sent_msg.encode(), client_addr)
        if counter == 10: 
            print("Connection lost")
    for sock in readready: 
        msg, client_addr = process_recvmsg(sock) 
        if state != 'idle':
            sent_msg = state_machine[state](sock,client_addr, msg)
