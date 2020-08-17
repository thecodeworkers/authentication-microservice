from .settings import Database, Server
from .utils import paginate, parser_all_object, parser_one_object, generate_salt
from .models import Roles, Users
from .providers.auth_provider import AuthProvider

class App():
    def __init__(self):
        init_database = Database()
        init_database.start_connection()

        auth = AuthProvider()
        auth = auth.provider
        print(auth.authorize('https://tcw', ('caceres.vc95@gmail.com', '123456')))


        # init_server = Server()
        # init_server.connection = init_database
        # init_server.start_server()
