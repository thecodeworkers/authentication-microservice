import os
from os.path import join, dirname
from dotenv import load_dotenv

path = os.path.dirname(dirname(__file__))
dotenv_path = join(path, '.env')

load_dotenv(dotenv_path)

DATABASE_NAME = os.getenv('DATABASE_NAME', 'resources')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_PORT = int(os.getenv('DATABASE_PORT', 27017))

SECURE_SERVER = os.getenv('SECURE_SERVER', 'True')
MAX_WORKERS = int(os.getenv('MAX_WORKERS', 5))
HOST = os.getenv('HOST', '[::]:50051')

SERVICEBUS_HOST = os.getenv('SERVICEBUS_HOST', 'localhost')
