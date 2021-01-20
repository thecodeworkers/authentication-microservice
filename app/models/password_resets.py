from mongoengine import Document, ReferenceField, StringField, DateTimeField, signals
from .auth import Auth
import datetime

class PasswordResets(Document):
    user = ReferenceField(Auth)
    token = StringField(min_length=60, max_length=300, required=True, unique=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def update(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(PasswordResets, self).save(*args, **kwargs)
