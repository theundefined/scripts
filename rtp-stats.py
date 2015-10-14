#!/usr/bin/python
from __future__ import with_statement
import socket
import sys
import pickle
import time
import re

ttl=60

def loadfromnetwork(ip,port):
    print >>sys.stderr, 'read from net'
    MESSAGE="I I"
    try:
        sock = socket.socket(socket.AF_INET,
            socket.SOCK_DGRAM)
        sock.settimeout(5)
        sock.sendto(MESSAGE, (ip, port))
        data, addr = sock.recvfrom(16000)
        sock.close()
    except IOError:
        print "network error"
        raise
    return data

def updatecache(ip,port):
    filename='/tmp/rtpstats-%s-%d.cache' % ( ip,port )
    data={}
    data["blob"]=loadfromnetwork(ip,port)
    data["epoch"]=time.time()
    with open(filename,'wb') as f:
        pickle.dump(data,f)
    return data

def loadcached(ip,port):
    filename='/tmp/rtpstats-%s-%d.cache' % ( ip,port )
    try:
        with open(filename,'rb') as f:
           data=pickle.load(f)
        if data["epoch"] + ttl < time.time():
            data=updatecache(ip,port)
    except (IOError,EOFError):
        data=updatecache(ip,port)
    return data

def parsesession(list=[]):
    r={}
    if list[0]=="C":
        r["callid"]=list[1]
        r["way"]="in"
    else:
        r["callid"]=list[0]
        r["way"]="out"
    for k in range(0 ,len(list)):
        if list[k]=="codecsA" or list[k]=="codecsB":
            if list[k+2] != "(null)":
                r["codec"]=list[k+2]
        if list[k]=="ttl":
            r["ttl"]=list[k+2]
    return r

def parse(blob):
    parseddata={}
    parseddata["sessions"]={}
    lines = repr(blob).split('\\n')
    for line in lines:
        splitedline=line.replace('\\t','').split(' ')
        if len(splitedline) <=1:
            continue
        if splitedline[0]=="active":
            parseddata["active " + splitedline[1]]=splitedline[2]
        elif splitedline[1]=="sessions":
            parseddata["created sessions"]=splitedline[3]
        else:
            session=parsesession(splitedline)
            if not session.has_key("callid"):
                # cos nie tak z linia
                continue
            if not parseddata["sessions"].has_key(session["callid"]):
                parseddata["sessions"][session["callid"]]={}
            parseddata["sessions"][session["callid"]][session["way"]]=session
#            parseddata["sessions"][session["callid"]][session["way"]]["raw"]=splitedline

#        for k in range(0 ,len(splitedline)):
#            print k,splitedline[k]
    return parseddata


def main():
    try:
        UDP_IP = sys.argv[1]
    except IndexError:
        UDP_IP = "10.0.0.2"
    UDP_PORT = 22222
    MESSAGE = "I I"
    data=loadcached(UDP_IP,UDP_PORT)
    parseddata=parse(data["blob"])
    for callid in parseddata["sessions"]:
        print callid, parseddata["sessions"][callid]

if __name__ == '__main__':
    main()
