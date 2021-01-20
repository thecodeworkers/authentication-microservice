from google.protobuf.json_format import MessageToDict
from ...protos import PasswordResetServicer, CreateTokenResponse, PasswordResetEmpty, PasswordResetEmpty, add_PasswordResetServicer_to_server
from ...utils import not_exist_code, update_or_create, hash_password
from ...models import PasswordResets, Auth
from ..bootstrap import grpc_server
import binascii
import datetime
import math
import os

class PasswordResetService(PasswordResetServicer):
    def create_token(self, request, context):
        try:
            user = Auth.objects.get(email=request.email)
            criteria = {'user': user}

            values = {
                **criteria,
                'token': binascii.hexlify(os.urandom(60)).decode()
            }

            password_reset = update_or_create(PasswordResets, criteria, values)
            return CreateTokenResponse(token=password_reset.token)

        except Auth.DoesNotExist as error:
            not_exist_code(context, error)

    def reset_password(self, request, context):
        try:
            password_reset = PasswordResets.objects.get(token=request.token)

            def delete_password_reset():
                return password_reset.delete()

            datetime_end = datetime.datetime.now()
            datetime_start = password_reset.updated_at

            minutes_diff = (datetime_end - datetime_start).total_seconds() / 60.0
            minutes_diff = math.floor(minutes_diff)

            if minutes_diff > 60:
                delete_password_reset()
                raise Exception('Token expired')

            user = password_reset.user
            user.password = hash_password(request.password)
            user.save()
            delete_password_reset()

            return PasswordResetEmpty()

        except PasswordResets.DoesNotExist as not_exist_err:
            not_exist_code(context, not_exist_err)
        except Exception as error:
            raise Exception(error)


def start_password_reset_service():
    add_PasswordResetServicer_to_server(PasswordResetService(), grpc_server)
