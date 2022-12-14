# 자기 목표 제안서

## 1. 자기 목표 제안서 설명

### 1) 자기설정목표

- **노트북, 라즈베리파이 간의 무선 데이터 통신으로 라즈베리파이에 연결된 센서 및 모터 원격 제어 구현**

  - 라즈베리파이에 연결된 서보모터(펜틸트), 초음파센서를 노트북(원격)으로 제어하고 센서 값을 확인함.
  - 무선망을 이용한 MQTT 프로토콜 통신 방법을 적용하여 서버/클라이언트 구현

### 2) 평가기준: 상(2pts) - 중(1pts) - 하(0pts) 기준

- **`상`: 노트북과 라즈베리파이의 MQTT 무선 통신 서버/클라이언트 구현, 무선통신을 통한 라즈베리 파이 센서 및 모터 간접(원격) 제어**

  - 펜틸트 값 송수신 및 제어: 노트북에서 MQTT 프로토콜을 이용하여 펜틸트 모터 제어 값을 라즈베리파이로 보내 라즈베리파이에 연결된 펜틸트 모터를 간접적으로 제어
  - 초음파 센서 값 송수신: 라즈베리파이에서 측정하는 초음파 센서 값을 MQTT 프로토콜을 이용하여 노트북으로 보내 노트북 클라이언트에서 초음파 값을 간접적으로 확인

- **`중`: 노트북과 라즈베리파이의 MQTT 무선 통신 서버/클라이언트 구현**

  - 펜틸트 값 송수신: 라즈베리파이에서 MQTT 통신을 통해 펜틸트 모터 제어 값을 라즈베리파이로 보내 라즈베리파이 노트북 클라이언트에서 제어 값을 간접적으로 확인
  - 초음파 센서 값 송수신: 라즈베리파이에서 제어하는 초음파 센서 값을 MQTT 통신을 통해 노트북 클라이언트에서 초음파 값을 간접적으로 확인

- **`하`: 노트북과 라즈베리파이의 간의 MQTT 무선통신 서버/클라이언트 구현이 미흡함.**

### 3) 구현 결과: `상(2pts)` (아래 [2.자기 목표 제안서 실천 과정](https://github.com/Sehee-Lee-01/2022_2_ESD/tree/main/GoalProject#2-%EC%9E%90%EA%B8%B0-%EB%AA%A9%ED%91%9C-%EC%A0%9C%EC%95%88%EC%84%9C-%EC%8B%A4%EC%B2%9C-%EA%B3%BC%EC%A0%95)을 참고해주세요!)

## 2. 자기 목표 제안서 실천 과정

### 1) MQTT 소개

- **MQTT(Message Queueing Telemetry Transport)란?**

  - `Publish-Subscribe`

    - 2016년 국제 표준화 된 (ISO 표준 ISO/IEC PRF 20922) 발행-구독(Publish-Subscribe) 기반의 메시지 송수신 프로토콜이다.
    - 소켓통신 같은 기능을 제공하는 라이브러리인 `Socket.io`와 조금 비슷한 것 같다.
    - `Broker`, `Publisher`, `Subscriber` 구조로 이루어진다.
      - `Broker`: `Publisher`와 `Subscriber`를 중게한다.
      - `Publisher`: Topic을 발행한다.
      - `Subscriber`: Topic을 구독한다.

  - `대역폭에 구애받지않는 원격 통신`

    - 작은 코드 공간이 필요하거나 네트워크 대역폭이 제한되는 원격 통신을 위해, 즉 IoT와 같은 제한된, 혹은 대규모 트래픽 전송을 위해 만들어진 프로토콜이다.

  - `가벼운 통신 환경`
    - TCP/IP 프로토콜 위에서 동작하지만 동시에 굉장히 가벼우며, 많은 통신 제약들을 해결해준다.
    - 최소한의 전력과 패킷량으로 통신한다.
    - IOT와 모바일 어플리케이션 등의 통신에 매우 적합하다.

- **MQTT의 특징**

  - `연결지향적(Connection Oriented)`
    - MQTT 브로커와 연결을 요청하는 클라이언트는 TCP/IP 소켓 연결을 한다. 명시적으로 연결을 끊거나 네트워크 사정에 의해 연결이 끊어질 때까지 상태를 유지한다.
  - `브로커를 통한 통신`
    - MQTT의 발행-구독 메시징 패턴은 오로지 브로커를 통해서만 통신할 수 있다.
    - 개설된 Topic에 메시지를 발행하면 브로커는 해당 Topic을 구독하는 클라이언트들에게 메시지를 발행할 수 있다. 일대일, 혹은 일대다의 통신이 모두 가능하다. (`Socket.io`와 비슷한 점이다.)
  - `QoS (Quality of Service)`

    - 브로커에 대한 각 연결은 QoS 기준을 지정할 수 있다. 부하가 늘어나는 순서에 따라 분류한다.
    - 이 필드는 기반이 되는 TCP 데이터 전송의 처리에 영향을 주지 않으며, MQTT 송신자와 수신자 간에만 사용된다.
    - 크게 3 단계로 이루어져 있다.
      - `0`
        - 메세지는 한 번만 전달한다.
        - 전달 이후 수신과정을 체크하지 않는다.
      - `1`
        - 메세지는 한 번 이상 전달된다.
        - 핸드셰이킹 과정을 추적하지만 엄격하게 추적하지 않는다.
        - 중복 수신의 가능성이 있다.
      - `2`
        - 메세지는 한 번만 전달된다.
        - 핸드셰이킹의 모든 과정을 체크한다.
    - 단계가 높아질 수록 통신 품질은 높아지지만 통신 성능이 저하될 수 있다는 Trade-Off가 있다.

  - `메세지의 유형`

    - 연결하기
    - 연결 끊기
    - 발행하기

  - `다양한 개발언어, 다양한 클라이언트 지원`
    - 언어에 구애받지 않고 구현할 수 있다.

### 2) MQTT 환경설정

MQTT 프로토콜을 이용하기 위해서는 MQTT Broker 프로그램이 필요하다. 여기서는 대표적으로 쓰이는 `Mosquitto`를 이용하여 진행하고자 한다.

- 노트북 설정
  - [Mosquitto 공식 홈페이지](https://mosquitto.org/download/)로 들어가서 해당 운영체제에 맞는 프로그램을 다운 받는다.
- 라즈베리파이 설정
  - [블로그](https://velog.io/@imkkuk/%EB%9D%BC%EC%A6%88%EB%B2%A0%EB%A6%AC%ED%8C%8C%EC%9D%B4-MQTT)를 참고하여 진행했다.

### 4) 노트북과 라즈베리파이의 MQTT 무선 통신 Publisher/Subscriber(Python)

 MQTT 프로토콜로 통신을 하기 위해서는 통신 전에 Mosquitto라는 MQTT 메세지 브로커를 실행해야한다.

- Mosquitto가 설치된 라즈베리파이나 노트북 터미널에 `mosquitto`를 입력한다.

- [기본 Pub/Sub 코드 링크](https://github.com/Sehee-Lee-01/2022_2_ESD/tree/main/GoalProject/MQTTBasic)
  - [Pub.py](https://github.com/Sehee-Lee-01/2022_2_ESD/blob/main/GoalProject/MQTTBasic/Pub.py)(Publisher): 정보를 보내는 주체에서 실행
  - [Sub.py](https://github.com/Sehee-Lee-01/2022_2_ESD/blob/main/GoalProject/MQTTBasic/Sub.py)(Subscriber): 정보를 받는 주체에서 실행

### 5) [펜틸트 값 송수신 및 원격 제어(영상 링크)](https://github.com/Sehee-Lee-01/2022_2_ESD/issues/4)

노트북에서 MQTT 프로토콜을 이용하여 펜틸트 모터 제어 값을 라즈베리파이로 보내 라즈베리파이에 연결된 펜틸트 모터를 간접적으로 제어

- [구현 결과 링크](https://github.com/Sehee-Lee-01/2022_2_ESD/tree/main/GoalProject/ServoMQTT)

- `Publisher(정보를 보내는 주체)`: 노트북(원격 컴퓨터)
  - `2022_2_ESD\GoalProject\ServoMQTT\Pub.py` 실행
  - 펜틸트 제어값을 입력하여 전송

- `Subscriber(정보를 받는 주체)`: 팬틸트가 연결된 라즈베리파이
  - `2022_2_ESD\GoalProject\ServoMQTT\Sub.py` 실행
  - 수신한 서보모터 제어값으로 팬틸트를 제어

### 6)  초음파 센서 값 송수신 및 원격 모니터링

라즈베리파이에서 측정하는 초음파 센서 값을 MQTT 프로토콜을 이용하여 노트북으로 보내 노트북 클라이언트에서 초음파 값을 간접적으로 확인

![image](https://user-images.githubusercontent.com/85275893/207810431-a9dc7a66-876f-4e1a-b865-e82d0a0bc00a.png)

- [구현 결과 링크](https://github.com/Sehee-Lee-01/2022_2_ESD/tree/main/GoalProject/UltraMQTT)

- `Publisher(정보를 보내는 주체)`: 초음파 센서가 연결된 라즈베리파이
  - `2022_2_ESD\GoalProject\UltraMQTT\Pub.py` 실행
  - 초음파 센서 값을 측정한 후 전송
  
- `Subscriber(정보를 받는 주체)`: 노트북(원격 컴퓨터)
  - `2022_2_ESD\GoalProject\UltraMQTT\Sub.py` 실행
  - 수신한 초음파 센서 값을 터미널에 출력
