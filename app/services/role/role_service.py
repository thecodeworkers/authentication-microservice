from google.protobuf.json_format import MessageToDict
from mongoengine.queryset import NotUniqueError
from ...protos import RoleServicer, RoleMultipleResponse, RoleResponse, RoleTableResponse, RoleEmpty, add_RoleServicer_to_server
from ...utils import parser_all_object, parser_one_object, not_exist_code, exist_code, paginate
from ...utils.validate_session import is_auth
from ...models import Roles
from ..bootstrap import grpc_server

class RoleService(RoleServicer):
    def table(self, request, context):
        metadata = dict(context.invocation_metadata())
        is_auth(metadata['auth_token'], '00_role_table')
        roles = Roles.objects
        response = paginate(roles, request.page)
        response = RoleTableResponse(**response)
        
        return response

    def get_all(self, request, context):
        metadata = dict(context.invocation_metadata())
        is_auth(metadata['auth_token'], '00_role_get_all')
        roles = parser_all_object(Roles.objects.all())
        response = RoleMultipleResponse(role=roles)

        return response

    def get(self, request, context):
        try:
            metadata = dict(context.invocation_metadata())
            is_auth(metadata['auth_token'], '00_role_get')
            role = Roles.objects.get(id=request.id)
            role = parser_one_object(role)
            response = RoleResponse(role=role)

            return response

        except Roles.DoesNotExist as e:
            not_exist_code(context, e)

    def save(self, request, context):
        try:
            metadata = dict(context.invocation_metadata())
            is_auth(metadata['auth_token'], '00_role_save')
            role_object = MessageToDict(request)
            role = Roles(**role_object).save()
            role = parser_one_object(role)
            response = RoleResponse(role=role)

            return response

        except NotUniqueError as e:
            exist_code(context, e)

    def update(self, request, context):
        try:
            metadata = dict(context.invocation_metadata())
            is_auth(metadata['auth_token'], '00_role_update')
            role_object = MessageToDict(request)
            role = Roles.objects(id=role_object['id'])

            if not role: del role_object['id']

            role = Roles(**role_object).save()
            role = parser_one_object(role)
            response = RoleResponse(role=role)
        
            return response

        except NotUniqueError as e:
            exist_code(context, e)
        
    def delete(self, request, context):
        try:
            metadata = dict(context.invocation_metadata())
            is_auth(metadata['auth_token'], '00_role_delete')
            role = Roles.objects.get(id=request.id)
            role = role.delete()
            response = RoleEmpty()

            return response

        except Roles.DoesNotExist as e:
            not_exist_code(context, e)

def start_role_service():
    add_RoleServicer_to_server(RoleService(), grpc_server)
