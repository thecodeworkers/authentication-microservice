from oauthlib.oauth1 import Client
from urllib.parse import parse_qsl
from .provider import server as provider
from ...models import Clients, RequestTokens
from ...utils import generate_salt, update_or_create

def create_request_tokens(uri, user):
    user_object = {
        'user': user.pk
    }

    client_object = {
        'client_key': generate_salt(25),
        'client_secret': generate_salt(30),
        'redirect_uri': uri,
        **user_object
    }

    client = update_or_create(Clients, user_object, client_object)

    default_url = client.redirect_uri

    oauth_client = Client(client.client_key, client_secret=client.client_secret, callback_uri=f'{default_url}/callback')
    uri, headers, body = oauth_client.sign(f'{default_url}/request_token')
    headers, body, status = provider.create_request_token_response(uri, body=body, headers=headers)

    if status > 200: raise Exception('Unauthorized')

    request_tokens = dict(parse_qsl(body))
    
    body = {
        **request_tokens,
        **client_object,
        'verifier': RequestTokens.objects.get(request_token_secret=request_tokens['oauth_token_secret']).verifier
    }

    return body
