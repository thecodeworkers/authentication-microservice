from google.protobuf.json_format import MessageToDict
from ..services.bootstrap import service_bus

def is_auth(token, scope):
    service_bus.init_connection()
    auth = service_bus.receive('validate_session', { 'authToken': token, 'scope': scope });
    service_bus.stop()
    service_bus.close_connection()

    if auth != True:
        raise Exception('Unauthorized') from None

def extract_token(request):
    request_dict = MessageToDict(request)
    key = 'authToken'
    token = ''

    if key in request_dict:
        token = request_dict['authToken']
        del request_dict['authToken']

    return (request_dict, token)
