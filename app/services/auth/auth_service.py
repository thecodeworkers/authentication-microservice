from google.protobuf.json_format import MessageToDict
from mongoengine.queryset import NotUniqueError
from ...protos import AuthServicer, add_AuthServicer_to_server, SignupResponse, SigninResponse
from ...utils import parser_one_object, not_exist_code, exist_code, hash_password, verify_password
from ...providers.auth_provider import AuthProvider
from ...models import Auth, Roles
from ..bootstrap import grpc_server

class AuthService(AuthServicer):
    def signup(self, request, context):
        try:
            information = MessageToDict(request)
            role = Roles.objects.get(code=information['role'])

            information['role'] = role
            if not information['password']:
                raise Exception('Password is empty')
            
            information['password'] = hash_password(information['password'])

            auth = Auth(**information).save()
            auth = {
                'email': auth.email,
                'username': auth.username
            }

            return SignupResponse(auth=auth)

        except NotUniqueError as e:
            exist_code(context, e)
        except Roles.DoesNotExist as e:
            not_exist_code(context, e)

    def signin(self, request, context):
        try:
            auth = self.__get_user_auth({ 'username': request.username })
            if not auth: auth = self.__get_user_auth({ 'email': request.username })
            if not auth: raise Exception('user not exist')

            if not verify_password(auth.password, request.password): raise Exception('password not match')

            provider = AuthProvider().provider
            token = provider.authorize(auth)

            auth = {
                'auth': {
                    'email': auth.email,
                    'username': auth.username
                },
                'authToken': token
            }

            return SigninResponse(**auth)

        except Exception as e:
            not_exist_code(context, e)

    def __get_user_auth(self, criteria):
        return Auth.objects(**criteria).first()


def start_auth_service():
    add_AuthServicer_to_server(AuthService(), grpc_server)
