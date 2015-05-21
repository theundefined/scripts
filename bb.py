#!/usr/bin/python
def wake_host(bcast, mac):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  content ='\xff'*6 + mac*16
  s.sendto(content, (bcast, 9))

