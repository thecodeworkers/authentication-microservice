from mongoengine import Document, StringField, ReferenceField
from .auth import Auth

class Clients(Document):
    client_key = StringField(max_length=300)
    client_secret = StringField(max_length=300)
    rsa_key = StringField(max_length=300)
    auth = ReferenceField(Auth)
    redirect_uri = StringField(max_length=300)
