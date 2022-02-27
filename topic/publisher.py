import pika
import random
from rich import print

# Create a connection, say CN
conn = pika.BlockingConnection(parameters=pika.ConnectionParameters(host="localhost"))
# Create a channel in CN, say CH
channel = conn.channel()
# Create a Topic Exchange
channel.exchange_declare(exchange="system_exchange", exchange_type="topic")
# Publish the message
severity = ("E", "W", "I", "O")
priority = ("H", "M", "L")
action = ("A1", "A2", "A3")
component = ("C1", "C2", "C3")

for _ in range(10):
    random_severity = severity[random.randint(0, len(severity)-1)]
    random_priority = priority[random.randint(0, len(priority) - 1)]
    random_action = action[random.randint(0, len(action) - 1)]
    random_component = component[random.randint(0, len(component) - 1)]

    rk = f"{random_severity}.{random_priority}.{random_action}.{random_component}"
    message = f"{rk} :::::<Message>"
    channel.basic_publish(exchange="system_exchange", routing_key=rk, body=message)
    print(f"[x] sent {message}")

# Close the connection Automatically closes the channel
channel.exchange_delete(exchange="system_exchange", if_unused=False)
conn.close()
