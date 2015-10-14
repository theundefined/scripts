#!/usr/bin/python
import socket
import sys
try:
    UDP_IP = sys.argv[1]
except IndexError:
    UDP_IP = "10.1.2.3"
UDP_PORT = 22222
MESSAGE = "I I"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET,
	socket.SOCK_DGRAM)
sock.settimeout(5)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

data, addr = sock.recvfrom(16000)
print "received message:", data
sock.close()
