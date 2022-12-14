# 2022년 2학기 임베디드시스템 설계 기말 프로젝트

## 0. Title: Object tracking & laser pointing system

- Difficulty: Expert

- Function: Track a tennis ball and shoot laser

- Library: Pigpio, OPENCV

- Additional Goal: PID servo control for smooth tracking

## 1. 주제 선택 동기

![임시설자료 (6)](https://user-images.githubusercontent.com/85275893/207628858-0ac79a5d-6525-4fe6-969c-9cc2a05e103e.png)

- 실시간으로 팬틸트 모터 제어를 해야하는 프로젝트가 이 프로젝트이기도 하고 테니스공을 인식하기위한 영상처리 과정도 흥미로울 것 같아서 이 프로젝트를 진행하게되었습니다.

## 2. 시스템 구조 및 핵심 기술 요소 소개

## 1) HW 부문

![임시설자료 (3)](https://user-images.githubusercontent.com/85275893/207603825-3e2736dc-25ea-4511-963b-bb3426a9964c.png)

![임시설자료 (14)](https://user-images.githubusercontent.com/85275893/207807389-531abd17-ed7f-4354-83f6-dde3016e3de4.png)

![임시설자료 (15)](https://user-images.githubusercontent.com/85275893/207807402-999378cc-e8fe-4660-8a76-160ac0d90375.png)

1) 컴퓨팅: `RaspberryPi 4 model b`
2) 서보모터: `MG90S 2개(x, y 축)` : 카메라가 객체를 따라가도록 제어
3) 서보 `팬틸트` kit: 서보모터 2개를 잘 세팅할 수 있는 키트

- X, Y 분리하여 제어

4) 레이저 모듈: 레이저가 감지된 객체를 가리킴 **(팬틸트 kit에 부착)**

- 항상 on
- 팬틸트에 직접 부착
- 카메라 방향과 평행

5) 카메라 모듈: 트래킹해야할 객체 감지를 위한 카메라 **(팬틸트 kit에 부착)**

- 항상 on
- 팬틸트에 직접 부착
- 레이저 방향과 평행

## 2) SW 부문 + 핵심 기술 요소([코드 보러가기](https://github.com/Sehee-Lee-01/2022_2_ESD/blob/main/FinalProject/ball_tracking.py))

- 테니스공 인식(`OpenCV`)

![임시설자료 (10)](https://user-images.githubusercontent.com/85275893/207807329-1947a616-5918-45b1-a41c-7f83630e2978.png)

- [테니스공 인식 참고 링크](https://pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/)

- HSV 필터 이용하여 테니스공 색깔 분리
  
- 테니스공 중앙값 찾은 후 좌표값 받기

- 테니스공 트래킹(pigpio)

![임시설자료 (11)](https://user-images.githubusercontent.com/85275893/207807350-45858bfd-0506-4000-974f-2b6461113fa1.png)
![임시설자료 (12)](https://user-images.githubusercontent.com/85275893/207807356-b0e932c0-9a34-49a3-8f85-1eb3c1cb1ca9.png)

- [객체 트래킹 로직 참고 링크](https://www.hackster.io/shubhamsantosh99/face-tracker-using-opencv-and-arduino-55412e)

- 화면 중앙 좌표값과 받은 좌표값 차이로 제어해야할 방향 정하기
- 계산된 방향으로 한 틱마다 정해진 단위로 이동
  
- `RPi.GPIO`가 아닌 `pigpio`로 서보모터 떨림 완화
  - pigpio를 사용하는 이유([링크](https://luigibox.tistory.com/entry/%EB%9D%BC%EC%A6%88%EB%B2%A0%EB%A6%AC%ED%8C%8C%EC%9D%B44-%EC%84%9C%EB%B3%B4%EB%AA%A8%ED%84%B0-SG-90-%EB%96%A8%EB%A6%BC%ED%9D%94%EB%93%A4%EB%A6%BC-jittershaking-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%ED%95%B4%EA%B2%B0-GPIO%EB%9D%BC%EC%9D%B4%EB%B8%8C%EB%9F%AC%EB%A6%AC)): 기존 RPi.GPIO와 다르게 pigpio는 로우레벨언어를 사용해 하드웨어 제어와 연산처리를 나누어 줘서 서로 간섭을 하지않게 하여 서보모터 제어시 떨림을 완화할 수 있다.
  - 프로젝트 실행 전에 `sudo pigpiod` 터미널에 입력

## 3. 동작 시연 링크([유튜브 영상](https://youtu.be/CVtfMwrFZrg))

https://user-images.githubusercontent.com/85275893/207807973-f4954919-8c85-4082-98ef-fb4ec7a38327.mov
