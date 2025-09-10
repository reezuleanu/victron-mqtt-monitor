from abc import ABC, abstractmethod


class BaseMonitor(ABC):
    """Class that continuously reads data from a Client and checks if any Alerts are triggered"""

    @abstractmethod
    def run() -> None:
        """Read from a client in an infinite loop and check alerts"""
