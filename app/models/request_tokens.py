from mongoengine import Document, StringField, ReferenceField
from .clients import Clients

class RequestTokens(Document):
    client = ReferenceField(Clients)
    request_token = StringField(max_length=300)
    request_token_secret = StringField(max_length=300)
    verifier = StringField(max_length=300)
