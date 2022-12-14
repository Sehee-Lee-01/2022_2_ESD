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


x = 7.5
y = 7.5

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
    
    diff_x = float(message)
    if (diff_x < 0):
        if x <=3:
            x = 3
        else:
            x = x - 1
    else:
        if x >= 12:
            x = 12
        else:
            x = x + 1
		
    
    print("x: ",x)
    # print("y: ",y)
    print("message: ",message)
    pwm_x.ChangeDutyCycle(float(x)) # for 반복문에 실수가 올 수 없으므로 /10.0 로 처리함. 
    #pwm_y.ChangeDutyCycle(float(y)) # for 반복문에 실수가 올 수 없으므로 /10.0 로 처리함.
    
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
