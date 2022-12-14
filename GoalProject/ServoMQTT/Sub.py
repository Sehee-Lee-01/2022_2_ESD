import RPi.GPIO as GPIO
import time

width = 640
height = 480

servo_pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)  # 50Hz (서보모터 PWM 동작을 위한 주파수)
pwm.start(3.0)  # 0.6ms

pwm.ChangeDutyCycle(7.5)  # 서보 모터를 90도로 회전(이동)


for i in range (0,3) :    
    for high_time in range (30, 125):
        pwm.ChangeDutyCycle(high_time/10.0) # for 반복문에 실수가 올 수 없으므로 /10.0 로 처리함. 
        time.sleep(0.02)
 
    for high_time in range (124, 30,-1):
        pwm.ChangeDutyCycle(high_time/10.0) # for 반복문에 실수가 올 수 없으므로 /10.0 로 처리함. 
        time.sleep(0.02)

pwm.ChangeDutyCycle(0.0)
pwm.stop()
GPIO.cleanup()

