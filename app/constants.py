import os
from os.path import join, dirname
from dotenv import load_dotenv

path = os.path.dirname(dirname(__file__))
dotenv_path = join(path, '.env')

load_dotenv(dotenv_path)

DATABASE_NAME = os.getenv('DATABASE_NAME', 'authentication')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_PORT = int(os.getenv('DATABASE_PORT', 27017))

SECURE_SERVER = os.getenv('SECURE_SERVER', 'True')
MAX_WORKERS = int(os.getenv('MAX_WORKERS', 5))
HOST = os.getenv('HOST', '[::]:50050')

SERVICEBUS_HOST = os.getenv('SERVICEBUS_HOST', 'localhost')
SERVICEBUS_SECURE = os.getenv('SERVICEBUS_SECURE', False)
SERVICEBUS_TIMEOUT = int(os.getenv('SERVICEBUS_TIMEOUT', 2))

PROVIDER = os.getenv('PROVIDER', 'oauth1')

JWT_SECRET = os.getenv('JWT_SECRET', 'JhbGciOiJIUzI1N0eXAiOiJKV1QiLC')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_LIFETIME = int(os.getenv('JWT_LIFETIME', 3600))
