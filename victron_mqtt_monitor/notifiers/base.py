from abc import ABC, abstractmethod


class BaseNotifier(ABC):
    @abstractmethod
    def notify(message: str) -> None:
        raise NotImplementedError
