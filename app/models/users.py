from mongoengine import Document, StringField, ReferenceField
from bson import json_util
from .roles import Roles

class Users(Document):
    email = StringField(max_length=150, required=True)
    username = StringField(max_length=150, required=True, unique=True)
    password = StringField(max_length=300, required=True, unique=True)
    role = ReferenceField(Roles, required=True)

    def to_json(self):
        data = self.to_mongo()

        data['role'] = {
            'id': str(self.role.id),
            'name': self.role.name,
            'code': self.role.code
        }

        return json_util.dumps(data)
