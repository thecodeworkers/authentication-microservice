from ...constants import JWT_SECRET, JWT_ALGORITHM, JWT_LIFETIME
from ...utils.status_code import not_exist_code
from ...models import Auth
from ..auth_interface import AuthInterface
import jwt
import datetime

class Jwt(AuthInterface):
    def authorize(self, auth):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_LIFETIME),
            'sub': auth.email
        }

        jwt_token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return jwt_token

    def validate_resource(self, access_token, scope=''):
        try:
            payload = jwt.decode(access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            auth = Auth.objects.get(email=payload['sub'])
            scopes = auth.role.scopes

            if scope in scopes: return str(auth.id)

            raise Exception('Unauthorized') from None

        except jwt.ExpiredSignatureError:
            raise Exception('Token expired') from None

        except Auth.DoesNotExist as e:
            raise Exception('Unauthorized') from None
