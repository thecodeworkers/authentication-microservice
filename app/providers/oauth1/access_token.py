from oauthlib.oauth1 import Client, ResourceEndpoint, SIGNATURE_PLAINTEXT
from urllib.parse import parse_qsl
from .provider import server as provider

def create_access_token(request_token):
    client = Client(
            request_token['client_key'], 
            client_secret=request_token['client_secret'], 
            resource_owner_key=request_token['oauth_token'], 
            resource_owner_secret=request_token['oauth_token_secret'], 
            verifier=request_token['verifier'],
            signature_method=SIGNATURE_PLAINTEXT
        )
    uri, headers, body = client.sign(f"{request_token['redirect_uri']}/access_token")

    headers, body, status = provider.create_access_token_response(uri, http_method='POST', body=body, headers=headers)
    access_tokens = dict(parse_qsl(body))

    return access_tokens
