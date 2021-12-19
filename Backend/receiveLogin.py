#!/usr/bin/env python
import pika, sys, os

def main():
    credentials = pika.PlainCredentials(username='anton', password='1234')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.24.122.108', credentials=credentials))
    # host = jp ipv4
    # added credentials=credentials
    channel = connection.channel()

    channel.queue_declare(queue='login')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='login', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)