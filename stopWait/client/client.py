#! /usr/bin/env python3

import os,re
import sys,time

from socket import *
from select import select 

server_addr = ('localhost', 50000)


def process_recvmsg(sock):
    global state
    msg, sender_addr = sock.recvfrom(102)
    msg = msg.decode()
    print("recived: %s"%msg)
    if state == 'wait': 
        if msg.find("ACK") == -1:
            process_get(sock, msg, sender_addr)


def process_get(sock, msg, sender_addr): 
    global state, requestfile
    openfile = open("files/"+requestfile, "a")
    msg_split = msg.split(":")
    openfile.write(msg_split[1])
    if msg_split[0] != "-1":
        msgto_send = "ACK:s"+msg_split[0]
        sock.sendto(msgto_send.encode(),sender_addr)
        state = 'wait'
    else: 
        msgto_send = "Thank you, Goodbye"
        sock.sendto(msgto_send.encode(), sender_addr)
        sock.close()
    return int(msg_split[0])
    

client_socket = socket(AF_INET, SOCK_DGRAM)

read_set = set([client_socket])
write_set = set()
error_set = set([client_socket])
timeout = 5

state = 'idle'

requestfile = "foo.txt"
getsent = False
while True: 
    readready, writeready, error = select(read_set, write_set, error_set, timeout)

    if not readready: 
        if state == 'idle' and not getsent:
            open("files/"+requestfile, "w+") # create file
            msgto_send = "GET:" + requestfile
            print("Send: %s"%msgto_send)
            client_socket.sendto(msgto_send.encode(), server_addr)
            state = 'wait'
    for sock in readready: 
        current_segment = process_recvmsg(sock)

