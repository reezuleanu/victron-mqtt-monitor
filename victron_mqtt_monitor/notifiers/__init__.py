from .email_notifier import EmailNotifier
from .base import BaseNotifier

from victron_mqtt_monitor.settings import config


def _build_notifiers() -> list[BaseNotifier]:
    """Build a list of enabled notifiers (based on config)"""

    conditions = [config.EMAIL_RECIPIENTS]
    notifiers = [EmailNotifier]

    notifiers = [
        notifier
        for condition, notifier in list(zip(conditions, notifiers))
        if condition
    ]

    return notifiers


enabled_notifiers = _build_notifiers()
