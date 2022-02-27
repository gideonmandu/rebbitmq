import pika
import sys
import os
from rich import print


def main():
    # Create a connection say CN
    conn = pika.BlockingConnection(pika.ConnectionParameters(host="0.0.0.0"))
    # Create a channel in CN, say CH
    channel = conn.channel()
    # Create the queue, if it does not exist already and associate it with the channel CH
    channel.queue_declare(queue="hello")

    def callback(ch, method, properties, body):
        print(fr"[x] received {body}")
    # Associate a call-back function with the message queue
    channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)
    # Start consuming the messages
    print("[x] waiting for the messages/ To exit press Ctrl + C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os.close(0)
