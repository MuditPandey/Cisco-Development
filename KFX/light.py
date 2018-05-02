#!/usr/bin/python

import time
import serial
import binascii
import sys
from sys import stdout
import os
import json

raw_dt=[]
rpt_cnt=0
ser_flag=0
reading=''

time_btw_chars=0.001
#time_btw_sets=0.100##delay b/w packets

ser=serial.Serial('/dev/ttyS1',baudrate=9600,timeout=0)
#ser=serial.Serial('/dev/ttyACM0',9600,timeout=0)


def get_temp():
	ser.flushInput()
	print ("Extracting Light Data")
	msg=b"::caSl0z"
	for j in range(0,len(msg)):
       		ser.write(msg[j])
		#print msg[j]	
		###ser.flush()
		time.sleep(0.003)
	ser.flush()
	time.sleep(0.3)
    	#read_resp()


def read_resp() :
	global ser_flag
	global rpt_cnt	
	global reading	
	clct_dt=0
	ser_flag=0	
	stime=time.time()
    	#while(1):
	while(ser_flag==0 and ser.inWaiting()>0):
	 #while(ser_flag==0 and ser.inWaiting()>0):	
		rec=ser.read()
		stdout.write(rec)
		if(rec==':'):
			clct_dt=1
			raw_dt=[':']
		elif(clct_dt==1):	
			raw_dt.append(rec)
			if(raw_dt[0]==':')and(rec=='z'):
				#print (raw_dt)
				reading=raw_dt[5:-1]
				#raw_dt[:]=[]
				clct_dt=0
				rpt_cnt=0
				ser_flag=1
	 #time.sleep(1.5)
		
def readfile(s_file):
   f_data=[]
   if(os.access(s_file,os.R_OK)) :
        f=open(s_file,'r')
        f_data=f.readlines()
        f.close()
   return f_data

def writefile(s_file, f_data):
   ### Add a file lock check
   f=open(s_file, 'w')
   for line in f_data :
        f.write(str(line) + "\n")
   f.close()
   ### Delete the file lock
   return

def appendfile(s_file, f_data):
   ### Add a file lock check
   f=open(s_file, 'a')
   for line in f_data :
        #f.write(str(line))
        f.write(str(line) + "\n")
   f.close()
   ### Delete the file lock
   return

def read_status() :
	cdata={}
	lines=readfile("scripts/status.txt")
	for line in lines :
		cline=line.strip()
		cdata=json.loads(cline)
	return cdata
   
ser_flag=0
rpt_cnt=0
ser.flush()
ser.flushInput()
ser.flushOutput()
get_temp()
read_resp()
for rpt_cnt in range(0,2):
	if(ser_flag!=1):
		#ser.flush()
		#ser.flushInput()
		#ser.flushOutput()
		get_temp()
		read_resp()
		rpt_cnt=rpt_cnt+1
		#print "SR ",ser_flag,"RC ",rpt_cnt	
ser.close()
#print (reading)
light=reading[0] + reading[1] +reading[2]
light=int(light)
light=light/60
#print (light)

cdata=read_status()
cdata['light']=light
writefile('scripts/status.txt',[json.dumps(cdata)])
