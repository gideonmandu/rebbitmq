import pika
from rich import print

# Create a connection, say CN
conn = pika.BlockingConnection(
    parameters=pika.ConnectionParameters(host="0.0.0.0"),
)
# Create a channel in CN, say CH
channel = conn.channel()
# [Optional] Create an Exchange
channel.exchange_declare(exchange="br_exchange", exchange_type="fanout")
# If the queue does not exist already
# Create a queue through the channel
# Publish the message
for i in range(4):
    message = f"Hello {i}."
    channel.basic_publish(exchange="br_exchange",routing_key="", body=message)
    print(f"[x] sent a message {message}")


channel.exchange_delete(exchange="br_exchange", if_unused=False)
# Close the connection
conn.close()
# Automatically closes the channel
