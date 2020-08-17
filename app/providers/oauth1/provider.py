from oauthlib.oauth1 import WebApplicationServer
from .validators import Oauth1RequestValidator

validator = Oauth1RequestValidator()
server = WebApplicationServer(validator)
