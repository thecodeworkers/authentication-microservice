from ..auth_interface import AuthInterface

class Jwt(AuthInterface):
    def authorize(self):
        return 'authorize jwt'

    def validate_resource(self):
        pass

