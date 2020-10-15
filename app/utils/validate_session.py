from ..providers.auth_provider import AuthProvider

def is_auth(token, scope):
    provider = AuthProvider().provider
    auth = provider.validate_resource(token, scope)

    if auth == '':
        raise Exception('Unauthorized') from None

    return auth
