# 라즈베리파이가 아닌 컴퓨터에서 실행, MQTT 프로토콜로 팬틸트 제어값 라즈베리파이로 지속적으로 전송
import paho.mqtt.client as mqtt
import time
import json

obj = 1
cordinate = 3
FLAG = False

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("completely connected")
    else:
        print("Bad connection Returned code=", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))

def on_publish(client, userdata, mid):
    print("In on_pub callback mid= ", mid)
    print("cordinate= ", cordinate)


client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

client.connect('localhost', 1883) # Mosquitto 브로커가 실행되고 있는 컴퓨터 IP

client.loop_start()

while True:
    time.sleep(0.1)
    client.publish('ServoData', cordinate, 1)
    
    if FLAG:
        if cordinate >= 12:
            FLAG = False
            continue			
        cordinate = cordinate + 1
	
    else:
        if cordinate <= 3:
            FLAG = True
            continue
        cordinate = cordinate - 1
		
		
client.loop_stop()

client.disconnect()
