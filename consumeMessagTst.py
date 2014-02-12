__author__ = 'Daniel'
import pika
from pprint import pprint

connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()
channel.queue_declare(queue='hello')

def callback(ch, method, propertis, body):
    pprint(body)

channel.basic_consume(callback, queue='traffic', no_ack=True)

channel.start_consuming()