from kafka import KafkaProducer
import os
import json

class Kafka:
    def __init__(self):
        kafkaEdgeServer =  os.environ.get('KAFKA_EDGE_SERVER')
        kafkaCloudServer =  os.environ.get('KAFKA_CLOUD_SERVER')

        if kafkaEdgeServer is None:
            print('Using 127.0.0.1 as default Kafka edge server.')
            kafkaEdgeServer='127.0.0.1'

        if kafkaCloudServer is None:
            print('Using 127.0.0.1 as default Kafka cloud server.')
            kafkaCloudServer='127.0.0.1'

        self.producer = KafkaProducer(bootstrap_servers=kafkaEdgeServer + ':9092', value_serializer=lambda v: v.encode('ascii'))

    def send(self, message):
        self.producer.send('Status', message)
