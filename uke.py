#!/usr/bin/python
from xml.dom import minidom
import re
import sys
import time
import pickle

if len(sys.argv) < 2:
    sys.stderr.write('Usage: sys.argv[0] numer\n')
    sys.exit(1)

numer=sys.argv[1]

def loaddata():
    #otwieramy plik w parserze
    DOMTree = minidom.parse('T1-PSTN.xml')
    cNodes = DOMTree.childNodes
    uke={}
    idn=0

    for i in cNodes[0].getElementsByTagName("pstn"):
#    <pstn>
#      <numer>SP=19</numer>
#      <strefa>
#        <nazwa>SN Krakow</nazwa>
#        <ab>12</ab>
#      </strefa>
#      <operator>Rezerwa techniczna</operator>
#      <obszar>CALA SN</obszar>
#      <blokada>false</blokada>
#    </pstn>

        uke[idn]={}
        uke[idn]["ab"]=i.getElementsByTagName("ab")[0].childNodes[0].wholeText.encode('ascii', 'ignore')
        uke[idn]["operator"]=i.getElementsByTagName("operator")[0].childNodes[0].wholeText.encode('ascii', 'ignore')
        t=i.getElementsByTagName("numer")[0].childNodes[0].wholeText.encode('ascii', 'ignore').split("=")
        uke[idn]["dopasowanie"]=t[0]
        #print "^" + uke[idn]["ab"] + t[1].replace("(","[").replace(")","]").replace(",","|"),uke[idn]["operator"]
        uke[idn]["reg"]="^" + uke[idn]["ab"] + "(" + t[1].replace("(","[").replace(")","]").replace(",","|").replace("-0","-90") + ")"
        uke[idn]["re"]=re.compile(uke[idn]["reg"])
    #    print idn,ab, numer, operator
        idn+=1
        # dostep do atrybutu
        #print i.getElementsByTagName("imie")[0].getAttribute("foo")
    return uke

epoch=time.time()
saveddata={}
try:
    f=open('/tmp/uke.cache','rb')
    saveddata=pickle.load(f)
except:
    saveddata['data']=loaddata()
    saveddata['epoch']=epoch
    pickle.dump(saveddata, open('/tmp/uke.cache', 'wb'))

if int(saveddata['epoch']) + 3600 < epoch:
#    print "refresh"
    saveddata['data']=loaddata()
    saveddata['epoch']=epoch
    pickle.dump(saveddata, open('/tmp/uke.cache', 'wb'))

uke=saveddata['data']

if numer=='-':
    for numer in sys.stdin:
        op=None
        for i in uke:
            if uke[i]["re"].match(numer):
                op=uke[i]["operator"]
        if op==None:
            print numer.strip() + ',nieznany'
        else:
            print numer.strip() + ',' + op
else:
    for i in uke:
        if uke[i]["re"].match(numer):
            print uke[i]["operator"]
