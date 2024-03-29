from mongoengine import EmbeddedDocument,Document
from mongoengine.fields import EmbeddedDocumentField,StringField,ListField, DateTimeField ,ReferenceField

class Quote(Document):
    tags = ListField()
    author = ReferenceField('Author')
    quote = StringField()
class Author(Document):
    fullname = StringField()
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()




