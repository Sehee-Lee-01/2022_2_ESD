import RPi.GPIO as GPIO
import time

servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin,GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(3.0)

for i in range (0,3) :    
    for high_time in range (30, 125):
        pwm.ChangeDutyCycle(high_time/10.0) # for 반복문에 실수가 올 수 없으므로 /10.0 로 처리함. 
        time.sleep(0.02)
    
    pwm.ChangeDutyCycle(3.0)    
    time.sleep(1.0)
    
pwm.ChangeDutyCycle(0.0)
pwm.stop()
GPIO.cleanup()
