#!/usr/bin/python

import os 
import sys
#import signal
import time

import requests
requests.packages.urllib3.disable_warnings()
from requests.auth import HTTPBasicAuth
import json
import base64

import serial

serial_port='/dev/ttyS2'
serial_baudrate = 115200

ser = serial.Serial(port=serial_port, baudrate=serial_baudrate, timeout=3, writeTimeout=3)

ping_url="http://54.218.121.4/atollkinesis/ak_service.php?ping=1&gatewayid=GW02&poll_time=15&gatewaytype=1&gw_batterystatus=100&main_pwr_sts=1"
data_up_url="http://54.218.121.4/atollkinesis/ak_service.php?gatewayid=GW02&networkid=ABCDEF&nodeid=201&nodetype=1&reserved=00&datalength=36&origin=110&poll_time=15&endflag=0&data="

serial_log_file = os.environ['CAF_APP_LOG_DIR'] + '/serial.log'
fp_serial       = open(serial_log_file,"a+b")
http_log_file = os.environ['CAF_APP_LOG_DIR'] + '/http_req.log'
fp_http= open(http_log_file,"a+b")

def get_timestamp():
    return str(time.ctime())

def read_serial():
    
    if ser.is_open:
        data_string=''
        while(True):    
            size = ser.inWaiting()
            
            if size > 0:
                
                data = ser.read(size)
                ndata = data.decode('utf-8')
                for ch in ndata:
                    if ch == '#' or ch =='\n':
                        continue
                    elif ch == '$':
                        if len(data_string) < 1:
                            continue
                        send_url = data_up_url + data_string
                        data_string =''
                        try:
                            request_data=requests.get(url=send_url,verify=False)
                            fp_http.write("[ "+get_timestamp()+" ] Sent GET http request to: "+send_url+"\n")
                            time.sleep(1)
                            fp_http.flush()
                        except requests.exceptions.RequestException as e:
                            fp_http.write("[ "+get_timestamp()+" ] "+str(e)+"\n")
                            time.sleep(1)
                            fp_http.flush()
                    else:
                        data_string = data_string + ch              
                fp_serial.write("[ "+get_timestamp()+" ] Read from Serial:"+str(ndata)+"\n")
                time.sleep(1)
                fp_serial.flush()
                fp_http.flush()
              
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
    
