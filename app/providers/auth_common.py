from ..models import Users

def validate_credentials(credentials):
    user, password = credentials
    current_user = Users.objects.get(email=user)

    if password != current_user.password:
        raise Exception('password not match')

    return current_user
