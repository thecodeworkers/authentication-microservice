from mongoengine import Document, StringField, ReferenceField
from .clients import Clients

class AccessTokens(Document):
    client = ReferenceField(Clients)
    access_token = StringField(max_length=300)
    access_token_secret = StringField(max_length=300)
