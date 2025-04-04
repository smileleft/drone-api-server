import asyncio
from gmqtt import Client as MQTTClient
import logging

# region callback functions
def on_connect(client, flags, rc, properties):
    logging.info("Connected to MQTT broker")
    client.subscribe('test/topic', qos=1)

def on_mission_connect(client, flags, rc, properties):
    logging.info("Connected to MQTT broker")
    client.subscribe('drone/commands', qos=1)

def on_message(client, topic, payload, qos, properties):
    logging.info(f"Received message on {topic}: {payload.decode()}")


def on_disconnect(client, packet, exc=None):
    logging.info("Disconnected from MQTT broker")
# endregion


# MQTT connect and publish
async def connect_and_publish():
    client = MQTTClient(client_id="python-client-123")

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    await client.connect(host='localhost', port=1883)

    # keep on (subscribe)
    while True:
        logging.info("Waiting for messages...")
        await asyncio.sleep(1)
        client.publish('test/topic', 'Hello from gmqtt!', qos=1)

# Drone mission test
async def do_mission_test():
    client = MQTTClient(client_id="drone-001")

    client.on_connect = on_mission_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    await client.connect(host='localhost', port=1883)

    while True:
        logging.info("Waiting for commands...")
        await asyncio.sleep(1)


# execute the main function
if __name__ == "__main__":
    #asyncio.run(connect_and_publish())
    asyncio.run(do_mission_test())