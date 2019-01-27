import time
import paho.mqtt.client as paho

broker="127.0.0.1"

client= paho.Client("controller") #create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")

#####
print("connecting to broker ",broker)
client.connect(broker)#connect
print("publishing ")
client.publish("leds","on")#publish
client.disconnect() #disconnect