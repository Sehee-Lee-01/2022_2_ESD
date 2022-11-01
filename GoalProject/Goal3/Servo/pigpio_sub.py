import paho.mqtt.client as mqtt
import json 
import pigpio as io
from time import sleep
import cv2

# pigpio
pix = io.pi()
piy = io.pi()

def SetServo(n):
    x = 600 + 10 * n
    return x

pix.set_servo_pulsewidth(18,0)
piy.set_servo_pulsewidth(23,0)

sleep(1)

x = 90
y = 90

pix.set_servo_pulsewidth(18,SetServo(x))
piy.set_servo_pulsewidth(23,SetServo(y))

XFLAG = 1


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
    global XFLAG
    
    message = str(msg.payload.decode("utf-8"))
    print(message)
    
    # parse json
    json_data = json.loads(message)
    obj_flag = int(json_data["obj_flag"])
	
    if obj_flag:
        diff_x = float(json_data["x_flag"])
        if (diff_x > 0):
            if x <= 0:
                x = 0
            else:
                x = x - 1
        else:
            if x >= 180:
                x = 180
            else:
                x = x + 1
            
        diff_y = float(json_data["y_flag"])
        if (diff_y > 0):
            if y <=0:
                y = 0
            else:
                y = y - 1
        else:
            if y >= 180:
                y = 180
            else:
                y = y + 1
    else:
        y = 90
        if (XFLAG == 0):
            if x <= 0:
                x = 0
                XFLAG = 1
            else:
                x = x - 1
        else:
            if x >= 180:
                x = 180
                XFLAG = 0
            else:
                x = x + 1
    print(x)
    print(y)
    pix.set_servo_pulsewidth(18,SetServo(x))
    piy.set_servo_pulsewidth(23,SetServo(y))
    
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message       

client.connect('10.3.60.134', 1883)
client.subscribe('test/hello', 1)
client.loop_forever()

 
# client.loop_stop()

pwm_x.stop()
pwm_y.stop()

GPIO.cleanup()
    
    
