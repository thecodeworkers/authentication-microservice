from oauthlib.oauth1 import Client, ResourceEndpoint
from .provider import server as provider, validator
from ..auth_interface import AuthInterface
from ..auth_common import validate_credentials
from ...models import Users, Clients
from ...utils import generate_salt, update_or_create

class Oauth1(AuthInterface):
    def authorize(self, uri, credentials):
        user = validate_credentials(credentials)
        
        user_object = {
            'user': user.pk
        }

        client_object = {
            'client_key': generate_salt(),
            'client_secret': generate_salt(30),
            'redirect_uri': uri,
            **user_object
        }

        client = update_or_create(Clients, user_object, client_object)

        client_key = client.client_key
        client_secret = client.client_secret
        default_url = client.redirect_uri

        oauth_client = Client(client_key, client_secret=client_secret, callback_uri=f'{default_url}/callback')
        uri, headers, body = oauth_client.sign(f'{default_url}/request_token')
        headers, body, status = provider.create_request_token_response(uri, body=body, headers=headers)

        ## Decodificar los tokens

        # Guardar en base de datos el client key y el client secret generados

        #Request tokens

        #Authorized Tokens

        return 'authorize oauth1'

    def validate_resource(self, access_token, scope):
        # Aqui solo recibo el access token, debo buscar en la base de datos y obtener tooodos los tokens necesarios para validar al usuario
        pass
