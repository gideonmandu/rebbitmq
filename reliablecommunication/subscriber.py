import time
import pika
import random
from rich import print


sub_id = random.randint(1, 100)
print(f"Subscriber Id: {sub_id}")
# Create a connection say CN
conn = pika.BlockingConnection(parameters=pika.ConnectionParameters(host="localhost"))
# Create a channel in CN, say CH
channel = conn.channel()
# Create the exchange (will not affect if exchange is already there)
channel.exchange_declare(exchange="logs_exchange", exchange_type="direct", durable=True)
# Create the queue, if it does not exist already and associate it with the channel CH
queue_name = "task_queue"
result = channel.queue_declare(queue=queue_name, durable=True)

# Bind the queue with the exchange for the required Routing Key(s)
severity = ("Error", "Warning", "Info", )
for s in severity:
    channel.queue_bind(exchange="logs_exchange", queue=queue_name, routing_key=s)
print("[*] waiting on messages")


# Associate a call-back function with the message queue
def callback(ch, method, properties, body):
    print(f"[x] Received message:::: {body}")
    random_sleep = random.randint(1, 5)
    print(f"Working for {random_sleep} seconds.")
    while random_sleep > 0:
        print(".", end="")
        time.sleep(1)
        random_sleep -= 1
    print("!")
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Start consuming the messages
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)
channel.start_consuming()
