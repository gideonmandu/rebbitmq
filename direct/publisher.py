import pika
import random
from rich import print

# Create a connection, say CN
conn = pika.BlockingConnection(parameters=pika.ConnectionParameters(host="localhost"))
# Create a channel in CN, say CH
channel = conn.channel()
# Create an Exchange
channel.exchange_declare(exchange="logs_exchange", exchange_type="direct")
# Publish the message
severity = ("Error", "Warning", "Info", "Other")
messages = ("EMsg", "WMsg", "IMsg", "OMsg")

for _ in range(10):
    randomNum = random.randint(0, len(severity)-1)
    print(randomNum)
    message = messages[randomNum]
    rk = severity[randomNum]
    channel.basic_publish(exchange="logs_exchange", routing_key=rk, body=message)
    print(f"[x] sent {message}")

# Close the connection Automatically closes the channel
channel.exchange_delete(exchange="logs_exchange", if_unused=False)
conn.close()
