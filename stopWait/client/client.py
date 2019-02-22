#! /usr/bin/env python3

import os,re
import sys,time

from socket import *
from select import select 

server_addr = ('localhost', 50000)

client_socket = socket(AF_INET, SOCK_DGRAM)




read_set = set([client_socket])
write_set = set()
error_set = set([client_socket])
timeout = 5

iput = sys.stdin.readline()[:-1]
while iput !=  "q":
    client_socket.sendto(iput.encode(), server_addr)
    msg, server_addr_port = client_socket.recvfrom(102)
    print(msg)
    iput = sys.stdin.readline()[:-1]


