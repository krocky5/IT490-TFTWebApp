#!/usr/bin/env python
# dis the file f
import pika, sys, os
from api import *

def rabbitReceive():
    credentials = pika.PlainCredentials(username='jp', password='1234')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.24.122.108', credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='api')

    def callback(ch, method, props, body):
        bodyToString = str(body)
        print(" [.] Riot Method(%s)" % bodyToString)
        

    channel.basic_consume(queue='api', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        rabbitReceive()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)