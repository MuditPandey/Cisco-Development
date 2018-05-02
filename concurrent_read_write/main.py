#!/usr/bin/python

import os 
import sys
#import signal
import time
from threading import Thread
import Queue

import serial
import paho.mqtt.client as mqtt

mqtt_server='173.39.91.122'
mqtt_port=1883
mqtt_pub_topic='tqb/serial_data'
mqtt_recv_topic='tqb/recv_data'

serial_port='/dev/ttyS1'
serial_baudrate=9600
ser = serial.Serial(port=serial_port, baudrate=serial_baudrate, timeout=3, writeTimeout=3)


mqtt_log_file   = os.environ['CAF_APP_LOG_DIR'] + '/mqtt.log'
fp_mqtt         = open(mqtt_log_file,"a+")

serial_log_file = os.environ['CAF_APP_LOG_DIR'] + '/serial.log'
fp_serial       = open(serial_log_file,"a+")

pub_msg_queue   = Queue.Queue()
recv_msg_queue  = Queue.Queue()

def get_timestamp():
 return str(time.ctime())
 
def on_connect(client,userdata,flags,rc):
    if rc == 0:
        fp_mqtt.write("[ "+ get_timestamp()+" ] (Read) Connection to server: "+mqtt_server+" successful!\n")
    else:
        fp_mqtt.write("[ "+get_timestamp()+" ] (Read) Connection to server: "+mqtt_server+" refused!\n")
    time.sleep(1)
    fp_mqtt.flush()
    client.subscribe(mqtt_recv_topic,0)    

def on_message(client,userdata,message):
    msg = message.payload.decode('utf-8')
    recv_msg_queue.put(str(msg))
    fp_mqtt.write("[ "+get_timestamp()+" ] (Read) Received message: "+ str(msg)+" on topic: "+ str(message.topic)+"\n")
    time.sleep(1)
    fp_mqtt.flush()
    
    if str(msg).lower() == 'log.reset':
        fp_mqtt.truncate(0)
        fp_serial.truncate(0)
        fp_mqtt.write("[ "+get_timestamp()+" ] File Reset was initiated. Log File reset!\n")
        fp_serial.write("[ "+get_timestamp()+" ] File Reset was initiated. Log File reset!\n")
        time.sleep(1)
        fp_serial.flush()
        fp_mqtt.flush()
        return
        
    if ~recv_msg_queue.empty():
        
        sdata=recv_msg_queue.get_nowait()
        
        try:            
            ser.write(str(sdata))
            fp_serial.write("[ "+get_timestamp()+" ] Wrote to Serial:"+str(sdata)+"\n")
            time.sleep(1)
            fp_serial.flush()
        except serial.SerialTimeoutException:
            fp_serial.write("[ "+get_timestamp()+" ] Write to Serial FAILED due to timeout\n")
            time.sleep(1)
            fp_serial.flush()
        except serial.SerialException:
            fp_serial.write("[ "+get_timestamp()+" ] Write to Serial FAILED due to unknown reason\n")
            time.sleep(1)
            fp_serial.flush()

            
def read_mqtt():
    mqtt_read_client=mqtt.Client()
    mqtt_read_client.connect(mqtt_server,mqtt_port)
    mqtt_read_client.on_connect = on_connect
    mqtt_read_client.on_message = on_message
    mqtt_read_client.loop_forever()

def write_mqtt():
    #mqtt_client.publish(mqtt_pub_topic,"START")
    #fp_mqtt.write("Published: START on topic: "+mqtt_pub_topic+"\n");
    #time.sleep(1)
    #fp_mqtt.flush()
    while(True):
        #data="hello"
        #mqtt_client.publish(mqtt_pub_topic,data)
        #fp_mqtt.write("Published: "+data+" on topic: "+mqtt_pub_topic+"\n");
        #time.sleep(1)
        #fp_mqtt.flush()
        if ~pub_msg_queue.empty():
            data = pub_msg_queue.get()
            mqtt_client=mqtt.Client()
            mqtt_client.connect(mqtt_server,mqtt_port)
            mqtt_client.publish(mqtt_pub_topic,data)
            fp_mqtt.write("[ "+get_timestamp()+" ] Published: "+str(data)+" on topic: "+mqtt_pub_topic+"\n");
            time.sleep(1)
            fp_mqtt.flush()
    fp_mqtt.close()

def read_serial():
    
    if ser.is_open:
        while(True):    
            size = ser.inWaiting()
            
            if size > 0:
                
                data = ser.read(size)
                ndata = data.decode('utf-8')
                pub_msg_queue.put(ndata)
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
if __name__=='__main__':
    th1 = Thread(target=read_serial, args = ())
    th1.start()
    
    th2 = Thread(target=write_mqtt, args = ())
    th2.start()
    
    th3= Thread(target=read_mqtt, args = ())
    th3.start()
    #read_serial()
    #write_mqtt()
    
