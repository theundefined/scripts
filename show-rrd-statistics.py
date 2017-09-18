#!/usr/bin/python
import rrdtool
import datetime
import calendar
import sys
def next_month(date):
	if date.month==12:
		nextmonth=1
		nextyear=date.year+1
	else:
		nextmonth=date.month+1
		nextyear=date.year

	return datetime.datetime(nextyear, nextmonth, 01, 0, 0)

def get_data(filename,start,end):
	delta=endepoch-startepoch
	return rrdtool.graph("/tmp/x.png","-s",'%s' % startepoch,'--end','%s' % endepoch,
			'DEF:in=%s:inputbytes:AVERAGE' % filename,
			'DEF:out=%s:outputbytes:AVERAGE' % filename,
			'VDEF:vin=in,TOTAL',
			'VDEF:vout=out,TOTAL',
			'PRINT:vin:%lf',
			'PRINT:vout:%lf')

#filename="file-eth0.17.rrd"
filename=sys.argv[1]
print '%s;%s;%s;%s;%s;%s' % ("nazwa pliku","od","do","ilosc czasu","ruch in","ruch out")
for year in range(2016,2018):
	for month in range(1,13):
		startdate=datetime.datetime(year, month, 01, 0, 0)
		enddate=next_month(startdate)
		startepoch=calendar.timegm(startdate.timetuple())
		endepoch=calendar.timegm(enddate.timetuple())
		delta=endepoch-startepoch
		#print startdate,enddate,delta,rrdtool.fetch(filename,'AVERAGE','-r','%s' % delta,'--start','%s' % startepoch,'--end','%s' % endepoch)
		x=get_data(filename,startepoch,endepoch)
		avgin=float(x[2][0])
		avgout=float(x[2][1])
#		if 'nan' not in avgin:
		print '%s;%s;%s;%ld;%ld;%ld' % (filename,startdate,enddate,delta,avgin,avgout)
