#! /usr/bin/env python3

import os,re
import sys,time

from socket import *
from select import select

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

def process_recvmsg(sock): 
    ''' Check wether if the client requested a 'GET' or 'PUT' '''
    msg, client_addr = sock.recvfrom(100)
    msg = msg.decode()
    if msg.find("GET") == 0: 
        get_file = msg[4:]
        send_file(sock,get_file,client_addr)
    elif msg.find("PUT") == 0: 
        save_file(sock)



server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(server_addr)

read_set = set()
write_set = set()
error_set = set()

timeout = 5

while True: 
    readready, writeready, error = select(read_set,write_set,error_set,timeout)

    for sock in readready: 
        process_recvmsg(sock)
