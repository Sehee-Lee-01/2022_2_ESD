# 필요한 패키지 import
from collections import deque
from imutils.video import VideoStream
# import pigpio as io # 서보모터를 좀 더 부드럽게 제어
import numpy as np
import argparse
import cv2
import time # 하드웨어 웜업과 라즈베리 파이 과부하 방지

# 인자 정의 및 인자 파싱 코드(버퍼 정의)
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

# 테니스 공의 색깔인 연두색의 범위를 정의
# HSV 컬러 범위에 있는 공이면 트랙 포인트 리스트(버퍼)를 초기화 한다.
# 버퍼의 자료구조는 deque이고 최대 길이는 위 인자에서 제시한 값으로 된다.
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])

cap = cv2.VideoCapture(0)

# 화면크기 조정
w = 640
h = 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)

# 화면의 센터 값 계산 
centerX = w//2
centerY = h//2
center = [centerX, centerY]   
bound_half = 30

# 트래킹 시작 전 하드웨어(비디오, 카메라) 웜업
time.sleep(2.0)

# 트래킹 시작
while True:
    # 실시간 처리를 위해, 라즈베리 과부하 방지를 위해 초당 15 프레임 처리하도록 설정
    time.sleep(0.07)

    # 현재 프레임을 읽는다.
    reg,frame = cap.read()

    # 읽은 프레임이 없는 경우 종료(T/F)
    if not reg:
        break

    # 영상을 블러처리하고 HSV color space로 변환
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # 위에서 정의한 연두색 마스크를 구성한다.
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # 큐에는 버퍼 크기만큼 과거의 센터 위치 정보들이 담겨있다.
    pts.appendleft(center)

    # loop over the set of tracked points
    # for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        # if pts[i - 1] is None or pts[i] is None:
            # continue

        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        # thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        # cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    
    # 움직이지 않아도 되는 범위 설정(흔들림 방지)
    cv2.rectangle(frame,(center[0]-bound_half,center[1]-bound_half),
                 (center[0]+bound_half,center[1]+bound_half),
                  (255,255,255),2)
    
    # 각종 표시가 들어간 프레임을 출력
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # 'q'키를 누르면 while문을 종료한다.
    if key == ord("q"):
        break

# 카메라를 닫고 메모리를 해제
cap.release()

# 모든 창 닫기
cv2.destroyAllWindows()