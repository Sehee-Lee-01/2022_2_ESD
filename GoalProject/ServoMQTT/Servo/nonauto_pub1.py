import paho.mqtt.client as mqtt
import time
import json

obj = 1
cordinate = 3
FLAG = False
direc = 0

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("completely connected")
    else:
        print("Bad connection Returned code=", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))

def on_publish(client, userdata, mid):
    print("In on_pub callback mid= ", mid)
    print("direc= ", direc)


client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

client.connect('192.168.0.58', 1883)

client.loop_start()

while True:
    time.sleep(0.1)
    direc = input("direction: ")
    client.publish('ServoData', direc, 1)
			
client.loop_stop()

client.disconnect()
