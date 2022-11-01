# 2022년 2학기 임베디드시스템 설계 기말 프로젝트

## 0. Title: Object tracking & laser pointing system

### - Difficulty: Expert

### - Function: Track a tennis ball and shoot laser

### - Library: OPENCV

### - Goal: PID servo control for smooth tracking

    * PID 코드 구현하기

## 1. 대표 HW 구성품

1) 컴퓨팅: `RaspberryPi 4 model b`
2) 서보모터: `MG90S 2개(x, y 축)` : 카메라가 객체를 따라가도록 제어
3) 서보 `팬틸트` kit: 서보모터 2개를 잘 세팅할 수 있는 키트
4) 레이저 모듈: 레이저가 감지된 객체를 가리킴 **(팬틸트 kit에 부착)**
5) 카메라 모듈: 트래킹해야할 객체 감지를 위한 카메라 **(팬틸트 kit에 부착)**

## 2. 개발환경 및 개발현황

### 1) HW 부문

- 서보모터 트래킹

  - 연결 테스트

  - `pigpio`로 코드 제어

- 레이저 모듈

  - 연결 테스트

  - on/off 코드 제어

- 라즈베리 파이 `카메라`

  - 라즈베리파이 연결 테스트: `dev/video*`로 나오는지 확인

  - `OpenCV` 연결 테스트: VideoCapture 연결 확인

- HW 제작

  - 카메라, 서보모터, 레이저 연결

### 2) SW 부문

- 객체 인식(`OpenCV`)

  - 특정 객체(공, 귤 등) 인식하고 박싱하는 코드 제작

  - 객체 박스 좌표값 받기

  - 화면 중앙 좌표값과 받은 좌표값 차이 확인

- 객체 트래킹

  - 좌표값 차이로 제어
