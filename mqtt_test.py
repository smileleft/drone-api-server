import asyncio
from gmqtt import Client as MQTTClient

# 이벤트 루프 (윈도우에서는 ProactorEventLoop 써야 할 수도 있음)
loop = asyncio.get_event_loop()

# 콜백 함수 정의
def on_connect(client, flags, rc, properties):
    print("Connected to MQTT broker")
    client.subscribe('test/topic', qos=1)

def on_message(client, topic, payload, qos, properties):
    print(f"Received message on {topic}: {payload.decode()}")

# MQTT 연결 함수
async def connect_and_publish():
    client = MQTTClient("python-client")

    client.on_connect = on_connect
    client.on_message = on_message

    await client.connect('localhost', 1883)

    await client.publish('test/topic', 'Hello from gmqtt!', qos=1)

    # 계속 실행 (subscribe 유지)
    while True:
        await asyncio.sleep(1)

# 실행
if __name__ == "__main__":
    asyncio.run(connect_and_publish())