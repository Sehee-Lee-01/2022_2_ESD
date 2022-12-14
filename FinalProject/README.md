# 2022년 2학기 임베디드시스템 설계 기말 프로젝트

## 0. Title: Object tracking & laser pointing system

### - Difficulty: Expert

### - Function: Track a tennis ball and shoot laser

### - Library: Pigpio, OPENCV

### - Additional Goal: PID servo control for smooth tracking

## 1. 대표 HW 구성품

1) 컴퓨팅: `RaspberryPi 4 model b`
2) 서보모터: `MG90S 2개(x, y 축)` : 카메라가 객체를 따라가도록 제어
3) 서보 `팬틸트` kit: 서보모터 2개를 잘 세팅할 수 있는 키트
4) 레이저 모듈: 레이저가 감지된 객체를 가리킴 **(팬틸트 kit에 부착)**
5) 카메라 모듈: 트래킹해야할 객체 감지를 위한 카메라 **(팬틸트 kit에 부착)**

## 2. 개발환경 및 개발현황

### 1) HW 부문

- 서보모터(팬틸트 모터)

  - GPIO가 아닌 `pigpio`로 섬세하게 제어
  - X, Y 분리하여 제어

- 레이저 모듈

  - 항상 on
  - 팬틸트에 직접 부착
  - 카메라 방향과 평행
  
- 라즈베리 파이 `카메라`

  - 항상 on
  - 팬틸트에 직접 부착
  - 레이저 방향과 평행

### 2) SW 부문

- 테니스공 인식(`OpenCV`)

  - [테니스공 인식 참고 링크](https://pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/)

  - 객체 박스 좌표값 받기

  - 화면 중앙 좌표값과 받은 좌표값 차이 확인

- 테니스공 트래킹
  - [객체 트래킹 로직 참고 링크](https://www.hackster.io/shubhamsantosh99/face-tracker-using-opencv-and-arduino-55412e)

  - 화면 중앙 좌표와 테니스공 중앙 좌표값 차이로 방향 제어
  - 계산된 방향으로 한 틱마다 정해진 단위로 이동
