#!/usr/bin/python
import time
import serial
import binascii
import sys
raw_dt=[]
rpt_cnt=0
ser_flag=0

time_btw_chars=0.0006
#time_btw_sets=0.100##delay b/w packets

ser=serial.Serial('/dev/ttyUSB0',baudrate=9600,timeout=0)
#ser=serial.Serial('/dev/ttyAMA0',9600,timeout=1)


def relay_II_low():
	print "Relay_II LOW"
	#msg=b":b20z"
	msg=b":cbR20z"
	for j in range(0,len(msg)):
       		ser.write(msg[j])
		#print msg[j]	
	time.sleep(0.1)
    	read_resp()


def read_resp() :
	time.sleep(0.100)
	clct_dt=0
	global ser_flag	
	ser_flag=0
	global rpt_cnt	
	stime=time.time()
    	#while(1):
    	while(ser.inWaiting()>0):
	 while(ser.inWaiting()>0):	
         	rec=ser.read()
		if(rec==':'):
			ser_flag=1
			clct_dt=1
		if(clct_dt==1):	
			raw_dt.append(rec)
			if(raw_dt[0]==':')and(rec=='z'):
				print raw_dt
				raw_dt[:]=[]
				clct_dt=0
				rpt_cnt=0
				ser_flag=1
	 time.sleep(1.5)
		
relay_II_low()
for rpt_cnt in range(0,3):
	if(ser_flag!=1):
		ser.flush()
		ser.flushInput()
		ser.flushOutput()
		relay_II_low()
		rpt_cnt=rpt_cnt+1
		#print "SR ",ser_flag,"RC ",rpt_cnt	
ser.close()
