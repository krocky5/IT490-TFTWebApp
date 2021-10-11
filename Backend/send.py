#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials(username='jp', password='1234')
#username password must match on rabbitmq management site
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='25.61.89.21', credentials=credentials))
#host ipv4 of where the server is
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body='jpjpjpjpjp!')
print(" [x] Sent 'Hello World!'")
connection.close()