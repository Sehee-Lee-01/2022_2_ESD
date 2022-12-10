import numpy as np
import cv2
import pigpio as io # 서보모터를 좀 더 부드럽게 제어
import time # 하드웨어 웜업과 라즈베리 파이 과부하 방지
import websockets
import asyncio
import time
import base64

# 프로그램 실행 전 아래 명령어 실행
# sudo pigpiod

# 영상 세팅 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
print("Setting camera...")

global WIDTH
global HEIGHT
global BOX_HALF
global center
global GREEN_LOWER
global GREEN_UPPER

cap = cv2.VideoCapture(0)

# 화면크기 조정
WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
print("WIDTH: " + str(WIDTH) + " HEIGHT: " + str(HEIGHT))

# 박스 바운더리 설정
BOX_HALF = 20

# 화면의 센터 값 계산(나중에는 공의 중심값 좌표가 들어감)
center = [WIDTH//2, HEIGHT//2]   

# 테니스 공의 색깔인 연두색의 범위를 정의
GREEN_LOWER = (29, 86, 6)
GREEN_UPPER = (64, 255, 255)

# 카메라 웜업
time.sleep(1.0)

# Pigpio 세팅 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
print("Setting pigpio...")


UNIT = 0.7 # 움직일 단위 설정

# 서보모터 각도 계산 및 변환
def SetServo(angle): 
    val = 600 + 10 * angle
    return val
    

# 서보모터 제어 구조체
x_pi = io.pi()
y_pi = io.pi()

# 서보모터 초기 값 설정
x_servo = 90
y_servo = 90
x_pi.set_servo_pulsewidth(17,SetServo(x_servo))
y_pi.set_servo_pulsewidth(27,SetServo(y_servo))
print("set!")

# 서보모터 웜업
time.sleep(1.0)


portNum = 6000
print("Started server on port : ", portNum)

# 트래킹 시작 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
async def streamServe(websocket, path):
    print("Client Connected !")
    while True:
        
        # 실시간 처리를 위해, 라즈베리 과부하 방지를 위해 
        # 초당 15 프레임 처리하도록 설정
        time.sleep(0.01)
        
        reg,frame = cap.read() # 현재 프레임을 읽는다.
        frame=cv2.flip(frame,1)  

        if not reg: # 읽은 프레임이 없는 경우 종료(T/F)
            break

        # 영상을 블러처리하고 HSV color space로 변환
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # 위에서 정의한 연두색 마스크를 구성한다.
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, GREEN_LOWER, GREEN_UPPER)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0]
        center = None
        
        if len(cnts) > 0: # 하나의 컨투어라도 찾으면 실행
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))   
            
            if radius > 10: # 공이 인식되고 반지름이 최솟값 이상일 경우 트래킹 동작
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2) # 공의 윤곽선        
                cv2.circle(frame, center, 5, (0, 0, 255), -1) # 공의 중심점
                print("Ball!")
                print("y: ", center[0] , " x: ", center[1])
                
                # 박스 바운더리 안에 오도록 트래킹 방향 계산
                if (center[0] > WIDTH//2 + BOX_HALF):
                    x_servo += UNIT
                elif (center[0] < WIDTH//2 - BOX_HALF):
                    x_servo -= UNIT
                    
                if (center[1] > HEIGHT//2 + BOX_HALF):
                    y_servo += UNIT
                elif (center[1] < HEIGHT//2 - BOX_HALF):
                    y_servo -= UNIT

                # if the servo degree is outside its range
                if (x_servo >= 180):
                    x_servo = 180
                elif (x_servo <= 0):
                    x_servo = 0
                
                if (y_servo >= 180):
                    y_servo = 180
                elif (y_servo <= 0):
                    y_servo = 0

                x_pi.set_servo_pulsewidth(17,SetServo(x_servo))
                y_pi.set_servo_pulsewidth(27,SetServo(y_servo))
                print("servo y: ", y_servo , "servo x: ", x_servo)

                
        # 움직이지 않아도 되는 범위 보여주기(흔들림 방지)
        cv2.rectangle(frame,(WIDTH//2-BOX_HALF,HEIGHT//2-BOX_HALF),
                    (WIDTH//2+BOX_HALF,HEIGHT//2+BOX_HALF),
                    (255,255,255),2)
        
        # 각종 표시가 들어간 프레임을 출력
        # cv2.imshow("Ball Tracking 20191987 이세희", frame)

        # 소켓으로 영상 전송
        encoded = cv2.imencode('.jpg', frame)[1]
        data = str(base64.b64encode(encoded))
        b64Data = data[2:len(data)-1]

        await websocket.send(b64Data)

        # 'q'키를 누르면 while문을 종료한다.
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    # 카메라를 닫고 메모리를 해제
    cap.release()
    # 모든 창 닫기
    # cv2.destroyAllWindows()

startServer = websockets.serve(streamServe, port=portNum)

asyncio.get_event_loop().run_until_complete(startServer)
asyncio.get_event_loop().run_forever()

cap.release()
