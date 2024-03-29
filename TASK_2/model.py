from mongoengine import Document
from mongoengine.fields import StringField, DateTimeField, ReferenceField, BooleanField


class Contact(Document):
    full_name = StringField()
    email = StringField()
    is_send_massage = BooleanField()
