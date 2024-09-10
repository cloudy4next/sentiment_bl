import os
import time
from dotenv import load_dotenv
import pickle
import pika

load_dotenv()

def declare(queues: list, channel):
    """Declare queues in RabbitMQ"""
    for queue in queues:
        channel.queue_declare(queue=queue)

def publish(queue: str, body: dict, channel, pickleit=True):
    """Publishes a message to the specified queue."""
    if pickleit:
        message = pickle.dumps(body)
    else:
        message = body
    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2  
                          ))

def consume(queue: str, callback, pickled=True):
    """Consume messages from a queue and process using the callback function."""
    def _consume(ch, method, properties, body):
        if pickled:
            body = pickle.loads(body)
        callback(ch, method, properties, body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    channel.basic_consume(queue=queue, on_message_callback=_consume)
    channel.start_consuming()

def connect(host):
    """Connect to RabbitMQ."""
    try:
        return pika.BlockingConnection(pika.ConnectionParameters(host=host))
    except Exception as e:
        print(f"Waiting for RabbitMQ connection: {e}")
        time.sleep(5)
        return None

if __name__ != "__main__":
    host = os.getenv("RABBITHOST", "localhost")
    connection = connect(host)
    while not connection:
        connection = connect(host)

    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
