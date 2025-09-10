from abc import ABC, abstractmethod

from victron_mqtt_monitor.notifiers import enabled_notifiers


class BaseAlert(ABC):

    def __init__(self):
        super().__init__()
        self.notifiers = enabled_notifiers
        self.alerted = False

    @abstractmethod
    def condition(self, data: dict) -> bool:
        """Defines the condition for the alert and
        returns if it's true or not"""

    @classmethod
    @abstractmethod
    def relevant_tag(cls) -> str: ...

    @classmethod
    @abstractmethod
    def required_data(cls) -> str: ...

    @abstractmethod
    def notify(self, data: dict) -> None:
        """Send an alert notification"""

    def reset(self) -> None:
        """Make alarm triggerable again"""

        self.alerted = False
