from .settings import Database, Server
from .utils import paginate, parser_all_object, parser_one_object
from .models import Roles, Users

class App():
    def __init__(self):
        init_database = Database()
        init_database.start_connection()

        # users = parser_one_object(Roles.objects.get(id="5f1a0749dcfcd16e4eb20841"))
        # print(users)

        init_server = Server()
        init_server.connection = init_database
        init_server.start_server()
