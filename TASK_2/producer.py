import pika
from faker import Faker
import argparse
import connect
from model import Contact
from datetime import datetime
import json

parser = argparse.ArgumentParser()
parser.add_argument("--countcontacts", "-cc", type=int)
args = parser.parse_args()

COUNT_GEN_CONTACTS = args.countcontacts if args.countcontacts != None else 10
print(COUNT_GEN_CONTACTS)


def generate_contacts(count_gen_contacts: int):
    faker = Faker()
    objects_id = list()
    for count in range(count_gen_contacts):
        contact = Contact(
            full_name=faker.name(), email=faker.email(), is_send_massage=False
        )
        contact.save()
        objects_id.append(contact.id)
    return objects_id


credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)

channel = connection.channel()

channel.exchange_declare(exchange="contact_exchange", exchange_type="direct")

channel.queue_declare(queue="contact_queue", durable=True)
channel.queue_bind(exchange="contact_exchange", queue="contact_queue")


def main(objects_id: list):
    counter = 0
    for oid in objects_id:
        counter += 1
        message = {
            "ObjectID": str(oid),
            "date": datetime.now().isoformat(),
        }
        channel.basic_publish(
            exchange="contact_exchange",
            routing_key="contact_queue",
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
        print(f"The task {message} has been queued.")
    connection.close()


if __name__ == "__main__":
    oid = generate_contacts(COUNT_GEN_CONTACTS)
    main(oid)
