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

mqtt_logfile=os.environ['CAF_APP_LOG_DIR']+'/mqtt.log'
fp_mqtt=open(mqtt_logfile,"a+")

pub_msg_queue= Queue.Queue()
recv_msg_queue= Queue.Queue()

def on_connect(client,userdata,flags,rc):
    if rc == 0:
        fp_mqtt.write("(Read) Connection to server: "+mqtt_server+" successful!\n")
    else:
        fp_mqtt.write("(Read) Connection to server: "+mqtt_server+" refused!\n")
    time.sleep(1)
    fp_mqtt.flush()
    client.subscribe(mqtt_pub_topic,0)    

def on_message(client,userdata,message):
    msg=message.payload.decode('utf-8')
    recv_msg_queue.put(str(msg))
    fp_mqtt.write("(Read) Received message: "+ str(msg)+" on topic: "+ str(message.topic)+"\n")
    time.sleep(2)
    fp_mqtt.flush()
            
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
            fp_mqtt.write("Published: "+str(data)+" on topic: "+mqtt_pub_topic+"\n");
            time.sleep(1)
            fp_mqtt.flush()
    fp_mqtt.close()

def read_serial():
    
    full_path = os.environ['CAF_APP_LOG_DIR'] + "/"+"serial.log"
    fp = open(full_path,"a+")
    ser= serial.Serial(port=serial_port,baudrate=serial_baudrate,timeout=10)
    if ser.is_open:
        while(True):    
            size = ser.inWaiting()
            fp.write(str(size)+"\n")
            time.sleep(1)
            fp.flush()
            if size > 0:
                data = ser.read(size)
                ndata = data.decode('utf-8')
                pub_msg_queue.put(ndata)
                fp.write("Read from Serial:"+str(ndata)+"\n")
                time.sleep(1)
                fp.flush()
            elif ~recv_msg_queue.empty():
                sdata=recv_msg_queue.get()
                ser.write(str(sdata))
                fp.write("Write to Serial:"+str(sdata)+"\n")
                time.sleep(1)
                fp.flush()
                #ser.write(str(ndata))   
            #time.sleep(1)
    else:
        fp.write("Serial not open!\n")
        time.sleep(1)
        fp.flush()
    fp.close()

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
    
