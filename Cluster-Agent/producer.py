from kafka import KafkaProducer
import time
import json

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda m: json.dumps(m).encode('utf-8'))
version = 'v1'
url = 'http://0.0.0.0:8000/api/show'

request_post = {
    'url': url,
    'type': 'POST',
    'data': {
        'name': "DANN-CODE",
        'entrance': "main/execute",
        'description': "",
        'mirrors': "{算法执行需要的镜像}"
    }
}

request_get = {
    'url': url,
    'type': 'GET'
}

print("Start producer...")
while True:
    producer.send('api-server', value=request_post, partition=0)
    producer.send('api-server', value=request_get, partition=0)
    time.sleep(5)
