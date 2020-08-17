from abc import ABC, abstractmethod

class AuthInterface(ABC):
    @abstractmethod
    def authorize(self):
        pass

    @abstractmethod
    def validate_resource(self):
        pass
