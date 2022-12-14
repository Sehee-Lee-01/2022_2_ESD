import paho.mqtt.client as mqtt
import json 
import RPi.GPIO as GPIO
import time




### GPIO setup
GPIO.setmode(GPIO.BCM)

servo_x_pin = 18
servo_y_pin = 23

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
    global FLAG
    global pwm_x
    global pwm_y
    message = str(msg.payload.decode("utf-8"))
    print(message)

    print("x: ",x)
    print("y: ",y)
    print("message: ",message)
    x = message
    pwm_x.ChangeDutyCycle(float(x))  
    pwm_y.ChangeDutyCycle(float(y)) 
    
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message       

client.connect('192.168.0.58', 1883)
client.subscribe('ServoData', 1)
client.loop_forever()

 
# client.loop_stop()

pwm_x.stop()
pwm_y.stop()

GPIO.cleanup()
