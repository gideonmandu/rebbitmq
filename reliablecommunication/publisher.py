import pika
import random
from rich import print

# Create a connection, say CN
conn = pika.BlockingConnection(parameters=pika.ConnectionParameters(host="localhost"))
# Create a channel in CN, say CH
channel = conn.channel()
channel.confirm_delivery()
# Create an Exchange
channel.exchange_declare(exchange="logs_exchange", exchange_type="direct", durable=True)
# Publish the message
severity = ("Error", "Warning", "Info", "Other")
messages = ("EMsg", "WMsg", "IMsg", "OMsg")

for _ in range(10):
    randomNum = random.randint(0, len(severity) - 1)
    print(randomNum)
    message = messages[randomNum]
    rk = severity[randomNum]
    try:
        channel.basic_publish(
            exchange="logs_exchange",
            routing_key=rk, body=message,
            properties=pika.BasicProperties(
                delivery_mode=2  # Make message persistent
            )
        )
        print(f"[x] sent {message}")
    except pika.exceptions.ChannelClosed:
        print("Channel closed")
    except pika.exceptions.ConnectionClosed:
        print("Connection Closed")

# Close the connection Automatically closes the channel
channel.exchange_delete(exchange="logs_exchange", if_unused=False)
conn.close()
