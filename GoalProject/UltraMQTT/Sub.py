# 라즈베리파이가 아닌 컴퓨터에서 실행, MQTT 프로토콜로 라즈베리파이에 연결된 초음파 센서 값 수신

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    print("ultraData from RaspberryPi>> ",str(msg.payload.decode("utf-8"))) # 라즈베리파이로부터 받은 초음파 센서 값


# 새로운 클라이언트 생성
client = mqtt.Client()
# 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_subscribe(topic 구독),
# on_message(발행된 메세지가 들어왔을 때)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message
# 로컬 아닌, 원격 mqtt broker에 연결
# address : broker.hivemq.com
# port: 1883 에 연결
client.connect('192.168.137.162', 1883) # Mosquitto 브로커가 실행되고 있는 컴퓨터 IP
# test/hello 라는 topic 구독
client.subscribe('ultraData', 1)
client.loop_forever()