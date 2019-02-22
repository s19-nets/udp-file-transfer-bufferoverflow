#! /usr/bin/env python3

import os,re
import sys,time

from socket import *

server_addr = ('localhost', 50000)

client_socket = socket(AF_INET, SOCK_DGRAM)

message = sys.stdin.readline()[:-1]
client_socket.sendto(message.encode(), server_addr)
msg, server_addr_port = client_socket.recvfrom(2048)
msg, server_addr_port = client_socket.recvfrom(2048)
print(msg)
message = sys.stdin.readline()[:-1]
client_socket.sendto(message.encode(), server_addr)
msg, server_addr_port = client_socket.recvfrom(2048)
print(msg)
message = sys.stdin.readline()[:-1]
client_socket.sendto(message.encode(), server_addr)
msg, server_addr_port = client_socket.recvfrom(2048)
print(msg)
message = sys.stdin.readline()[:-1]
client_socket.sendto(message.encode(), server_addr)
msg, server_addr_port = client_socket.recvfrom(2048)
print(msg)
