from mongoengine import Document, StringField, ReferenceField
from .users import Users

class Clients(Document):
    client_key = StringField(max_length=300)
    client_secret = StringField(max_length=300)
    rsa_key = StringField(max_length=300)
    user = ReferenceField(Users)
    redirect_uri = StringField(max_length=300)
