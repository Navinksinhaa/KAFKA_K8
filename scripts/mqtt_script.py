import paho.mqtt.client as mqtt
from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    event = {
        "deviceId": msg.topic.split('/')[-1],
        "value": payload,
        "timestamp": "2025-07-10T14:00:00Z"
    }
    producer.send('iot-events', event)
    print(f"Sent to Kafka: {event}")

client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.subscribe("sensors/#")
client.on_message = on_message
client.loop_forever()
