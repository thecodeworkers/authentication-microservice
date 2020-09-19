from ..models import Roles
from ..settings import Database

def role_seeder():
    database = Database()
    database.start_connection()

    roles = [
        {
            'name': 'admin',
            'code': '000',
            'scopes': []
        },
        {
            'name': 'basic_user',
            'code': '001',
            'scopes': []
        }
    ]

    for role in roles:
        exist_role = Roles.objects(code=role['code'])
        if not exist_role: Roles(**role).save()

    database.close_connection()
