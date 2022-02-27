import pika
from rich import print

# Create a connection say CN
conn = pika.BlockingConnection(pika.ConnectionParameters(host="0.0.0.0"))
# Create a channel in CN, say CH
channel = conn.channel()
# Create the exchange (will not affect if exchange is already there)
channel.exchange_declare(exchange="br_exchange", exchange_type="fanout")
#  #  Create the queue, if it does not exist already and associate it with the channel CH
# Create the temporary queue, if it does not exist already and associate it with the channel CH exclusively
result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue
print(f"Subscriber queue name {queue_name}")
# Bind the queue with the exchange
channel.queue_bind(exchange="br_exchange", queue=queue_name)
print("[*] waiting for the messages")
# Associate a call-back function with the message queue
def callback(ch, method, properties, body):
    print(rf"[x] {body}")


# Start consuming the messages
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True,
)

channel.start_consuming()
