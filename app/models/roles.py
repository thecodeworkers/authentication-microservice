from mongoengine import Document, StringField

class Roles(Document):
    name = StringField(max_length=255, required=True, unique=True)
    code = StringField(max_length=4, required=True)
    description = StringField(max_length=300)
