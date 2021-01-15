from google.protobuf.json_format import MessageToDict
from mongoengine.queryset import NotUniqueError
from ...protos import RoleServicer, RoleMultipleResponse, RoleResponse, RoleTableResponse, RoleEmpty, add_RoleServicer_to_server
from ...utils import parser_all_object, parser_one_object, not_exist_code, exist_code, paginate, parser_context, pagination, default_paginate_schema
from ...utils.validate_session import is_auth
from ...models import Roles, Auth
from bson.objectid import ObjectId
from ..bootstrap import grpc_server


class RoleService(RoleServicer):
    def table(self, request, context):
        auth_token = parser_context(context, 'auth_token')
        is_auth(auth_token, '00_role_table')

        roles = Roles.objects

        search = request.search

        pipeline = [
            {
                "$match": {
                    "$or": [
                        {"name": {"$regex": search, "$options": "i"}},
                        {"code": {"$regex": search, "$options": "i"}},
                    ]
                }
            },
            {
                "$group": {
                    "_id": "$_id",
                    "id": {"$first": {"$toString": "$_id"}},
                    "name": {"$first": "$name"},
                    "code": {"$first": "$code"},
                    "scopes": {"$first": "$scopes"},
                }
            },
            {
                "$project": {
                    "_id": 0
                }
            }
        ]

        pipeline = pipeline + pagination(request.page, request.per_page, {"name": 1})

        response = Roles.objects().aggregate(pipeline)

        response = RoleTableResponse(**default_paginate_schema(response, request.page, request.per_page))

        return response

    def get_all(self, request, context):
        auth_token = parser_context(context, 'auth_token')
        is_auth(auth_token, '00_role_get_all')

        roles = parser_all_object(Roles.objects.all())
        response = RoleMultipleResponse(role=roles)

        return response

    def get(self, request, context):
        try:
            auth_token = parser_context(context, 'auth_token')
            is_auth(auth_token, '00_role_get')

            role = Roles.objects.get(id=request.id)
            role = parser_one_object(role)
            response = RoleResponse(role=role)

            return response

        except Roles.DoesNotExist as e:
            not_exist_code(context, e)

    def save(self, request, context):
        try:
            auth_token = parser_context(context, 'auth_token')
            is_auth(auth_token, '00_role_save')

            role_object = MessageToDict(request)
            role = Roles(**role_object).save()
            role = parser_one_object(role)
            response = RoleResponse(role=role)

            return response

        except NotUniqueError as e:
            exist_code(context, e)

    def update(self, request, context):
        try:
            auth_token = parser_context(context, 'auth_token')
            is_auth(auth_token, '00_role_update')

            role_object = MessageToDict(request)
            role = Roles.objects(id=role_object['id'])

            if not role:
                del role_object['id']

            role = Roles(**role_object).save()
            role = parser_one_object(role)
            response = RoleResponse(role=role)

            return response

        except NotUniqueError as e:
            exist_code(context, e)

    def delete(self, request, context):
        try:
            auth_token = parser_context(context, 'auth_token')
            is_auth(auth_token, '00_role_delete')

            user = Auth.objects(role=request.id)

            if len(user) > 0:
                raise Exception('role_assigned')

            role = Roles.objects.get(id=request.id)
            role = role.delete()
            response = RoleEmpty()

            return response

        except Roles.DoesNotExist as e:
            not_exist_code(context, e)


def start_role_service():
    add_RoleServicer_to_server(RoleService(), grpc_server)
