import json
import requests
from kafka import KafkaConsumer

hosts = ['localhost:9092']
topic = ['api-server']

consumer = KafkaConsumer(bootstrap_servers=hosts,
                         value_deserializer=lambda v: json.loads(v.decode('utf-8')))
consumer.subscribe(topic)

print("Start agent...")
while True:
    for message in consumer:
        req = message.value
        if req.get('type').upper() == 'GET':
            r = requests.get(url=req.get('url'))
            print(r.text)
        if req.get('type').upper() == 'POST':
            r = requests.post(url=req.get('url'), data=req.get('data'))
            print(r.text)
