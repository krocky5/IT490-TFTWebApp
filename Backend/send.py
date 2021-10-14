#!/usr/bin/env python
import pika
from api import *

# testing this:
sumInfo = riotAPI.main()
str_sumInfo = ''.join(sumInfo)

credentials = pika.PlainCredentials(username='jp', password='1234')
#username password must match on rabbitmq management site
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.24.122.108', credentials=credentials))
#host ipv4 of where the server is
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body=str_sumInfo)
print(" [x] Sent 'Hello World!'")
connection.close()