# 왼오 -> 오왼 코드 완성하기.
# 각도 값을 변환해서 아예 그거로 써도 될 것 같다.
# 시그모이드 함수
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

pos_center = 7.5 #<- fill this using the answer for Question 3.

pwm = GPIO.PWM(17,50)  # (channel, frequency)
pwm.start(pos_center)

while True:
    try:
        raw_input = input("Duty (in %):")
        duty = float(raw_input)
        pwm.ChangeDutyCycle(duty)
	
    except ValueError:
    	print("Please enter a real number in percent.")

pwm.stop()
GPIO.cleanup()
