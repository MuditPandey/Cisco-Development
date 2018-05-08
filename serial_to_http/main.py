#!/usr/bin/python

import os 
import sys
#import signal
import time

import serial

serial_port='/dev/ttyS1'
serial_baudrate = 115200

ser = serial.Serial(port=serial_port, baudrate=serial_baudrate, timeout=3, writeTimeout=3)

serial_log_file = os.environ['CAF_APP_LOG_DIR'] + '/serial.log'
fp_serial       = open(serial_log_file,"a+b")

def get_timestamp():
    return str(time.ctime())

def read_serial():
    
    if ser.is_open:
        while(True):    
            size = ser.inWaiting()
            
            if size > 0:
                
                data = ser.read(size)
                ndata = data.decode('utf-8')
                fp_serial.write("[ "+get_timestamp()+" ] Read from Serial:"+str(ndata)+"\n")
                time.sleep(1)
                fp_serial.flush()
              
                #ser.write(str(ndata))   
            #time.sleep(1)
    else:
        fp_serial.write("[ "+get_timestamp()+" ] Serial not open!\n")
        time.sleep(1)
        fp_serial.flush()
    fp_serial.close()

#read_serial()
if __name__ == '__main__':

    read_serial()
    
