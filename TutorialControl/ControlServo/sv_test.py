# 왼오 -> 오왼 코드 완성하기.
# 각도 값을 변환해서 아예 그거로 써도 될 것 같다.
# 시그모이드 함수
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

pos_center = 7.5 #<- fill this using the answer for Question 3.

pwm = GPIO.PWM(17,50)  # (channel, frequency)
pwm.start(pos_center)

FLAG = True
curr_pos = pos_center

while True:
    try:
        #raw_input = input("Duty (in %):")
        # duty = float(raw_input)
        # pwm.ChangeDutyCycle(duty)
        time.sleep(0.01)
        if FLAG:
            if curr_pos >= 12:
                FLAG = False
                continue
            curr_pos= curr_pos + 0.1
        else:
            if curr_pos <= 3:
                FLAG = True
                continue
            curr_pos = curr_pos - 0.1
        print(curr_pos)
        print(FLAG)
        pwm.ChangeDutyCycle(float(curr_pos))
	
    except ValueError:
    	print("Please enter a real number in percent.")

pwm.stop()
GPIO.cleanup()
