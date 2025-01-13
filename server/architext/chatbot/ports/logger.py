import abc

class Logger(abc.ABC):
    @abc.abstractmethod
    def log(self, text: str) -> None:
        pass