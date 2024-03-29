import pika
import sys
import json
from model import Contact
import connect
from mongoengine.errors import DoesNotExist

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

channel.queue_declare(queue="contact_queue", durable=True)

print("[*] Waiting for messages. To exit PRESS CTRL+C")


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    object_id = message["ObjectID"]
    try:
        contact = Contact.objects.get(id=object_id)
        contact.update(is_send_massage=True)
        print(f"Received message for contact: {contact.full_name}")
    except DoesNotExist:
        print(f"Contact with ID: {object_id} not found in the database.")


channel.basic_consume(
    queue="contact_queue", on_message_callback=callback, auto_ack=True
)


if __name__ == "__main__":
    channel.start_consuming()
