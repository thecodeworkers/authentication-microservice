from oauthlib.oauth1 import Client, ResourceEndpoint
from .provider import server as provider, validator
from .request_token import create_request_tokens
from ..auth_interface import AuthInterface
from ..auth_common import validate_credentials
from ...models import Users
from ...utils import generate_salt, update_or_create

class Oauth1(AuthInterface):
    def authorize(self, uri, credentials):
        user = validate_credentials(credentials)
        request_token = create_request_tokens(uri, user)

        client = Client(
            request_token['client_key'], 
            client_secret=request_token['client_secret'], 
            resource_owner_key=request_token['oauth_token'], 
            resource_owner_secret=request_token['oauth_token_secret'], 
            verifier=request_token['verifier']
        )
        uri, headers, body = client.sign(f"{request_token['redirect_uri']}/access_token")

        headers, boby, status = provider.create_access_token_response(uri, http_method='POST', body=body, headers=headers)
        print(boby)

        # oauth_token = b['oauth_token'][0]
        # oauth_token_secret = b['oauth_token_secret'][0]

        #Request tokens

        #Authorized Tokens

        return 'authorize oauth1'

    def validate_resource(self, access_token, scope):
        # Aqui solo recibo el access token, debo buscar en la base de datos y obtener tooodos los tokens necesarios para validar al usuario
        pass
