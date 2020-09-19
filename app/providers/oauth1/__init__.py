from oauthlib.oauth1 import Client, ResourceEndpoint
from .provider import server as provider, validator
from .request_token import create_request_tokens
from .access_token import create_access_token
from ..auth_interface import AuthInterface
from ...models import AccessTokens
from ...utils import generate_salt, update_or_create

class Oauth1(AuthInterface):
    def authorize(self, auth, uri='https://tcw.com'):
        request_token = create_request_tokens(uri, auth)
        access_token = create_access_token(request_token)

        return access_token['oauth_token']

    def validate_resource(self, access_token, scopes=''):
        try:
            access_token_instance = AccessTokens.objects.get(access_token=access_token)
            client_instance = access_token_instance.client

            client = Client(
                client_instance.client_key, 
                client_secret=client_instance.client_secret,
                resource_owner_key=access_token,
                resource_owner_secret=access_token_instance.access_token_secret
            )
            uri, headers, body = client.sign(f'{client_instance.redirect_uri}/protected_resource')

            current_provider = ResourceEndpoint(validator)
            validate, request = provider.validate_protected_resource_request(uri, body=body, headers=headers, realms=[scopes])

            return validate

        except AccessTokens.DoesNotExist as error:
            raise Exception('Client not found') from None
