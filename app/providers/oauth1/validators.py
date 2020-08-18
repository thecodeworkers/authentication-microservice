from oauthlib.oauth1 import RequestValidator
from oauthlib.common import safe_string_equals
from ...models import Clients, RequestTokens
from ...utils import generate_salt, update_or_create

class Oauth1RequestValidator(RequestValidator):
    def get_default_realms(self, client_key, request):
        return []

    def validate_timestamp_and_nonce(self, client_key, timestamp, nonce, request, request_token=None, access_token=None):
        return True

    def validate_client_key(self, client_key, request):
        try:
            self.__get_current_client(Clients, {'client_key': client_key})
            return True

        except Clients.DoesNotExist as error:
            raise Exception('Client not found') from None

    def validate_requested_realms(self, client_key, realms, request):
        return True

    def validate_redirect_uri(self, client_key, redirect_uri, request):
        try:
            client = self.__get_current_client(Clients, {'client_key': client_key})

            if client.redirect_uri in redirect_uri:
                return True
            return False

        except Clients.DoesNotExist as error:
            return False
    
    def get_client_secret(self, client_key, request):
        try:
            client = self.__get_current_client(Clients, {'client_key': client_key})
            return client.client_secret

        except Clients.DoesNotExist as error:
            raise Exception('Client not found') from None

    def save_request_token(self, token, request):
        try:
            client = self.__get_current_client(Clients, {'client_key': request.client_key})

            client_object = {
                'client': client.id
            }

            request_token_object = {
                'request_token': token['oauth_token'],
                'request_token_secret': token['oauth_token_secret'],
                'verifier': generate_salt(),
                **client_object
            }

            update_or_create(RequestTokens, client_object, request_token_object)

        except Clients.DoesNotExist as error:
            raise Exception('Client not found') from None

    def validate_request_token(self, client_key, token, request):
        try:
            request_token = self.__get_current_client(RequestTokens, {'request_token': token})
            
            if request_token.client.client_key == client_key:
                return True

            raise Exception('Client not found') from None

        except RequestTokens.DoesNotExist as error:
            raise Exception('Client not found') from None

    def validate_verifier(self, client_key, token, verifier, request):
        request_token = self.__get_current_client(RequestTokens, {'request_token': token})

        if safe_string_equals(verifier, request_token.verifier):
            if request_token.client.client_key == client_key:
                return True

        return False

    def get_request_token_secret(self, client_key, token, request):
        try:
            request_token = self.__get_current_client(RequestTokens, {'request_token': token})
            
            if request_token.client.client_key == client_key:
                return request_token.request_token_secret

            raise Exception('Client not found') from None

        except RequestTokens.DoesNotExist as error:
            raise Exception('Client not found') from None




    def __get_current_client(self, model, key_value):
        return model.objects.get(**key_value)
