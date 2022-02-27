import pika
from rich import print


def fact(n):
    return 1 if n <= 1 else n * fact(n - 1)


def on_request(ch, method, props, body):
    reply_queue_name = props.reply_to
    corr_id = props.correlation_id
    n = int(body)
    print(f"Called fact {n}")
    response = fact(n)

    ch.basic_publish(
        exchange="",
        routing_key=reply_queue_name,
        properties=pika.BasicProperties(
            correlation_id=corr_id,
        ),
        body=str(response)
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)


# Create a connection say CN
conn = pika.BlockingConnection(parameters=pika.ConnectionParameters(host="localhost"))
# Create a channel in CN, say CH
channel = conn.channel()
# Create the exchange (will not affect if exchange is already there)
# Create the queue, if it does not exist already and associate it with the channel CH
queue_name = "rpc_server_queue"
result = channel.queue_declare(queue=queue_name, durable=True)

# Bind the queue with the exchange for the required Routing Key(s)
# Start consuming the messages
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=on_request)
print("[*] Awaiting on RPC requests")
channel.start_consuming()
