from abc import ABC, abstractmethod


class BaseNotifier(ABC):
    @abstractmethod
    def notify() -> None:
        raise NotImplementedError
