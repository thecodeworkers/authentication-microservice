from .role import start_role_service
from .auth import start_auth_emit

def start_all_servicers():
    start_role_service()

def start_all_emiters():
    start_auth_emit()
