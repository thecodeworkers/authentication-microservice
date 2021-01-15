from mongoengine import Document, StringField, ReferenceField, DateTimeField
from bson import json_util
from .roles import Roles

class Auth(Document):
    email = StringField(min_length=5,max_length=150, required=True, unique=True)
    username = StringField(max_length=150, required=False, unique=True, sparse=True)
    password = StringField(min_length=5,max_length=400, required=True)
    email_verification = DateTimeField()
    role = ReferenceField(Roles, required=True)

    def to_json(self):
        data = self.to_mongo()

        data['role'] = {
            'id': str(self.role.id),
            'name': self.role.name,
            'code': self.role.code
        }

        return json_util.dumps(data)
