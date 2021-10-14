#!/usr/bin/env python
import pika
from api import *

# sumInfo 
sumInfo = riotAPI.main()

# casting tuple to a string
str_sumInfo = ''.join(sumInfo)

credentials = pika.PlainCredentials(username='jp', password='1234')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.24.122.108', credentials=credentials))

channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body=str_sumInfo)
print(" [x] Sent 'Hello World!'")
connection.close()