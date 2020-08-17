from ..utils import dynamic_import

class AuthProvider():
    _provider_name = ''
    provider = None

    def __init__(self, provider='oauth1'):
        self._provider_name = provider
        self.__boot()

    def __boot(self):
        class_name = self._provider_name.capitalize()
        exchange_class = dynamic_import(f'app.providers.{self._provider_name}.{class_name}')
        self.provider = exchange_class()
