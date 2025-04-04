import asyncio
from gmqtt import Client as MQTTClient


# 콜백 함수 정의
def on_connect(client, flags, rc, properties):
    print("Connected to MQTT broker")
    client.subscribe('test/topic', qos=1)

def on_message(client, topic, payload, qos, properties):
    print(f"Received message on {topic}: {payload.decode()}")

def on_disconnect(client, packet, exc=None):
    print("Disconnected from MQTT broker")


# MQTT 연결 함수
async def connect_and_publish():
    client = MQTTClient(client_id="python-client-123")

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    await client.connect(host='localhost', port=1883)

    
    # 계속 실행 (subscribe 유지)
    while True:
        print("Waiting for messages...")
        await asyncio.sleep(1)
        client.publish('test/topic', 'Hello from gmqtt!', qos=1)

# 실행
if __name__ == "__main__":
    asyncio.run(connect_and_publish())