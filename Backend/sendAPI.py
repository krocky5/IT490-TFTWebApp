#!/usr/bin/env python

# code built from : https://www.rabbitmq.com/tutorials/tutorial-one-python.html
import pika
from api import *

# sumInfo - Calls main() object from riotAPI class
sumInfo = riotAPI.main()

# casting tuple to a string
str_sumInfo = ','.join(sumInfo)

# my login info for RabbitMQ
credentials = pika.PlainCredentials(username='jp', password='1234')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.24.122.108', credentials=credentials))

channel = connection.channel()

# Declaring a queue named 'api'
channel.queue_declare(queue='api')

channel.basic_publish(exchange='', routing_key='api', body=str_sumInfo)
print(" [x] Summoner Information Sent ")
connection.close()