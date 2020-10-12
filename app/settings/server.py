from ..services import grpc_server, service_bus, start_all_servicers, start_all_emiters
from ..constants import SECURE_SERVER, HOST
from .logger import logging
import grpc
import time
import sys
import os

class Server():
    def __init__(self):
        self.connection = None
        self.__secure_server = SECURE_SERVER
        self.__up_servicebus = 0

    def start_server(self):
        start_all_servicers()
        start_all_emiters()

        self.__set_correct_server()

    def __set_private_keys(self):
        with open('keys/private.key', 'rb') as f:
            private_key = f.read()

        with open('keys/cert.pem', 'rb') as f:
            public_key = f.read()

        server_credentials = grpc.ssl_server_credentials(
            ((private_key, public_key),)
        )

        return server_credentials

    def __set_correct_server(self):
        try:
            if self.__secure_server == 'False':
                grpc_server.add_insecure_port(HOST)
                logging.info('The server was unsecure')

            if self.__secure_server == 'True':
                credentials = self.__set_private_keys()
                grpc_server.add_secure_port(HOST, credentials)
                logging.info('The server was secure')

            grpc_server.start()
            logging.info(f'Starting server. Listening on {HOST}')
            self.__loop_server()

        except Exception as error:
            logging.error(error)

    def __determinate_loop(self):
        status = service_bus.status()

        if status:
            self.__up_servicebus = 1
            service_bus.start()
        else:
            while True:
                time.sleep(1)

    def __loop_server(self):
        try:
            self.__determinate_loop()

        except KeyboardInterrupt:
            grpc_server.stop(0)

            if self.__up_servicebus:
                service_bus.stop()
                service_bus.close_connection()

            self.connection.close_connection()
