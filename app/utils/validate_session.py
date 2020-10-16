from ..providers.auth_provider import AuthProvider
from bson import objectid

def is_auth(token, scope):
    provider = AuthProvider().provider
    auth = provider.validate_resource(token, scope)

    if not objectid.ObjectId.is_valid(auth):
        raise Exception(auth) from None

    return auth
