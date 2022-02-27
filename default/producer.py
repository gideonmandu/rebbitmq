import pika
from rich import print

# Create a connection, say CN
conn = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="0.0.0.0",
        # port=5672,
    )
)
# Create a channel in CN, say CH
channel = conn.channel()
# [Optional] Create an Exchange
# Specify the bindings
# If the queue does not exist already
# Create a queue through the channel
channel.queue_declare(queue="hello")
# Publish the message
channel.basic_publish(exchange="", routing_key="hello", body=b"HeLlO wOrLd #1")
print("[x] sent HeLlO wOrLd")
# Close the connection
conn.close()
# Automatically closes the channel
