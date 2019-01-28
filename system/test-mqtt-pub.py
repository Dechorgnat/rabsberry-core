#!/usr/bin/python
import paho.mqtt.client as paho
import argparse

broker="127.0.0.1"

parser=argparse.ArgumentParser(
        description='''MQTT test utility ''',
        epilog="""""")
parser.add_argument('--channel', default='leds', choices=['leds', 'ears'])
parser.add_argument('msg', nargs='+',  help='text message')
args=parser.parse_args()

client= paho.Client("controller") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")

#####
print("connecting to broker ",broker)
client.connect(broker)#connect
print("publishing ")
client.publish(args.channel, args.msg[0])#publish
client.disconnect() #disconnect
