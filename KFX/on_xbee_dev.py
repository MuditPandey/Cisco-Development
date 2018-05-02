#!/usr/bin/python
import time
import serial
import binascii
import sys
from sys import stdout

ser=serial.Serial('/dev/ttyUSB0',baudrate=9600,timeout=0)

while (1):
     	
	ser.flushInput()
	print "Relay_I HIGH"
	#msg=b":b11z"
	#msg=b":A108030351" # ON
	#msg=b":A108030054" #off
	msg=b":24080303CE" # ON
	for j in range(0,len(msg)):
		ser.write(msg[j])
		time.sleep(0.005)		
		#print msg[j]	
	time.sleep(0.1)
	break 	
ser.close()
