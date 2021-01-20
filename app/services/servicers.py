from .role import start_role_service
from .auth import start_auth_emit, start_auth_service
from .password_reset import start_password_reset_service

def start_all_servicers():
    start_role_service()
    start_auth_service()
    start_password_reset_service()

def start_all_emiters():
    start_auth_emit()
