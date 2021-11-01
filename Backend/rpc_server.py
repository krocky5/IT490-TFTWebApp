#!/usr/bin/env python
# This is hosted on jp's laptop
import pika
from api import *

credentials = pika.PlainCredentials(username='jp', password='1234')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.24.122.108', credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')

def on_request(ch, method, props, body):

    body=body.decode('utf-8')
    print(body)
    body = RiotAPI.main(body)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()