import RPi.GPIO as GPIO
import time
servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50Hz (서보모터 PWM 동작을 위한 주파수)
pwm.start(3.0) #서보의 0도 위치(0.6ms)이동:값 3.0은 pwm주기인 20ms의 3%를 의미하므로,0.6ms됨.
timeA = 0.6

for cnt in range(0, 3) :       # 0부터 3미만까지(3번) for문의 내용을 반복
    pwm.ChangeDutyCycle(3.0)   # 서보모터를 0도로 회전(이동)
    time.sleep(timeA)            # 서보 모터가 이동할 시간을 줌
    pwm.ChangeDutyCycle(5.5)  # 서보 모터를 45도로 회전(이동)
    time.sleep(timeA)            # 서보 모터가 이동할 시간을 줌
    pwm.ChangeDutyCycle(7.5)  # 서보 모터를 90도로 회전(이동)
    time.sleep(timeA)            # 서보 모터가 이동할 시간을 줌
    pwm.ChangeDutyCycle(9.5)  # 서보 모터를 135도로 회전(이동)
    time.sleep(timeA)            # 서보 모터가 이동할 시간을 줌    
    pwm.ChangeDutyCycle(12.5)  # 서보 모터를 180도로 회전(이동)
    time.sleep(timeA)            # 서보 모터가 이동할 시간을 줌
    pwm.ChangeDutyCycle(9.5)  # 서보 모터를 135도로 회전(이동)
    time.sleep(timeA)            # 서보 모터가 이동할 시간을 줌    
    pwm.ChangeDutyCycle(7.5)  # 서보 모터를 90도로 회전(이동)
    time.sleep(timeA)            # 서보 모터가 이동할 시간을 줌
    pwm.ChangeDutyCycle(5.5)  # 서보 모터를 45도로 회전(이동)
    time.sleep(timeA)            # 서보 모터가 이동할 시간을 줌
    pwm.ChangeDutyCycle(3.0)   # 서보모터를 0도로 회전(이동)
    time.sleep(timeA)            # 서보 모터가 이동할 시간을 줌

pwm.ChangeDutyCycle(0.0)
pwm.stop()
GPIO.cleanup()
