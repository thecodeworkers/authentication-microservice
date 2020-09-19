from .role import start_role_service
from .auth import start_auth_emit, start_auth_service

def start_all_servicers():
    start_role_service()
    start_auth_service()

def start_all_emiters():
    start_auth_emit()
