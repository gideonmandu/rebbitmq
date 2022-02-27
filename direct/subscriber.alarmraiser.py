import pika
from rich import print

# Create a connection say CN
conn = pika.BlockingConnection(parameters=pika.ConnectionParameters(host="localhost"))
# Create a channel in CN, say CH
channel = conn.channel()
# Create the exchange (will not affect if exchange is already there)
channel.exchange_declare(exchange="logs_exchange", exchange_type="direct")
# Create the queue, if it does not exist already and associate it with the channel CH
result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue
# Bind the queue with the exchange for the required Routing Key(s)
severity = ("Error", "Warning", "Info", )
channel.queue_bind(exchange="logs_exchange", queue=queue_name, routing_key="Error")
channel.queue_bind(exchange="logs_exchange", queue=queue_name, routing_key="Warning")
print("[*] waiting on messages")


# Associate a call-back function with the message queue
def callback(ch, method, properties, body):
    print(f"[x] Alarm:::: {body}")


# Start consuming the messages
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
