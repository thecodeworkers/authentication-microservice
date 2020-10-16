from ..channel import service_bus_connection
from ...providers.auth_provider import AuthProvider

class AuthEmitter():
    def __init__(self):
        self.__start_emitters()

    def emit_validate_session(self):
        service_bus_connection.add_queue('validate_session', self.__validate_session)

    def __validate_session(self, data):
        try:
            provider = AuthProvider().provider
            is_auth = provider.validate_resource(data['authToken'], data['scope'])

            return is_auth

        except Exception as error:
            return str(error)

    def __start_emitters(self):
        self.emit_validate_session()

def start_auth_emit():
    AuthEmitter()
    service_bus_connection.send()
