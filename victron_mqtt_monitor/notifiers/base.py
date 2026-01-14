from abc import ABC, abstractmethod

from victron_mqtt_monitor.interfaces import NotificationMessage


class BaseNotifier(ABC):
    @classmethod
    @abstractmethod
    def notify(cls, message: NotificationMessage) -> None:
        raise NotImplementedError
