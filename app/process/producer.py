import pika
import json

def publish(message):
    param=pika.URLParameters("amqps://pgmqkkhl:DC516D0tzh9OnHejzCbzyyh3VaJJUIxE@kangaroo.rmq.cloudamqp.com/pgmqkkhl")
    connection=pika.BlockingConnection(param)
    channel=connection.channel()
    channel.basic_publish(exchange="REQUEST_EXCHANGE",routing_key="RESPONSE_ROUTING_KEY",body=json.dumps(message))