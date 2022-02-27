import uuid
import pika
from rich import print


class FactRPCClient:
    def __init__(self):
        # Create a connection, say CN
        self.response = None
        self.correlation_id = None
        self.conn = pika.BlockingConnection(parameters=pika.ConnectionParameters(host="localhost"))
        # Create a channel in CN, say CH
        self.channel = self.conn.channel()
        self.queue_name = "rpc_client_queue"
        self.server_queue_name = "rpc_server_queue"
        self.channel.queue_declare(queue=self.queue_name, exclusive=True)

        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

    def on_response(self, ch, method, props, body):
        """Callback function"""
        if self.correlation_id == props.correlation_id:
            self.response = body

    def call(self, num: int):
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        # Publishing message to server
        self.channel.basic_publish(
            exchange="",
            routing_key=self.server_queue_name,
            properties=pika.BasicProperties(
                reply_to=self.queue_name,
                correlation_id=self.correlation_id,
            ),
            body=str(num),
        )
        while self.response is None:
            # waiting for response from server
            self.conn.process_data_events()
        return int(self.response) if self.response else None


fact_rpc = FactRPCClient()
n = 5

print(f"Requesting Fact {n}")
response = fact_rpc.call(n)
print(f"Got the response {response}")
