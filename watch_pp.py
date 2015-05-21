#!/usr/bin/python
import suds
import suds.wsse
import sys
import timeit
import getopt
import csv
url="https://tt.poczta-polska.pl/Sledzenie/services/Sledzenie?wsdl"
username="sledzeniepp"
password="PPSA"

def show_data(client,numer):
    spr=client.service.sprawdzPrzesylke(numer)
    if not spr.danePrzesylki:
        print "Brak przesylki %s" % (numer,)
        return
    for i in spr.danePrzesylki.zdarzenia[0]:
        print numer,i.czas, i.jednostka.nazwa, i.kod, i.nazwa

if len(sys.argv) > 1:
    numery=list(sys.argv[1:])
else:
    numery={
            'RQ260561184SG' : 'fasttech',
            }

security = suds.wsse.Security()
token = suds.wsse.UsernameToken(username,password)
security.tokens.append(token)
client=suds.client.Client(url)
client.set_options(wsse=security)
for numer in numery:
    show_data(client,numer)
