# 라즈베리파이에서 실행, MQTT 프로토콜로 받은 값(범위: 3~12)으로 서보모터 제어
# X, Y 동일한 각도로 제어

import paho.mqtt.client as mqtt
import json 
import RPi.GPIO as GPIO
import time

### GPIO setup
GPIO.setmode(GPIO.BCM)

servo_x_pin = 17
servo_y_pin = 27

GPIO.setup(servo_x_pin,GPIO.OUT)
GPIO.setup(servo_y_pin,GPIO.OUT)


pwm_x = GPIO.PWM(servo_x_pin, 50)
pwm_y = GPIO.PWM(servo_y_pin, 50)

FLAG = False


x = 3
y = 3

pwm_x.start(float(x))
pwm_y.start(float(y))

### MQTT setup
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))

def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    global x
    global y
    global pwm_x
    global pwm_y

    # 받은 메세지 파싱
    angle = str(msg.payload.decode("utf-8")) 
    print("angle: ",angle)

    # 받은 값으로 서보모터 제어
    x = float(angle) 
    y = float(angle)
    pwm_x.ChangeDutyCycle(x)  
    pwm_y.ChangeDutyCycle(y) 
    
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message       

client.connect('localhost', 1883) # Mosquitto 브로커가 실행되고 있는 컴퓨터 IP
client.subscribe('ServoData', 1)
client.loop_forever()

 
# client.loop_stop()

pwm_x.stop()
pwm_y.stop()

GPIO.cleanup()
