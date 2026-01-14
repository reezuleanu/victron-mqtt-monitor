from i18n import t

from victron_mqtt_monitor.alerts.base import BaseAlert
from victron_mqtt_monitor.interfaces import BatteryInfo, NotificationMessage


class BatteryAlert(BaseAlert):
    def __init__(self, threshold: float):
        super().__init__()
        self.threshold = threshold

    def condition(self, data) -> None:
        battery = BatteryInfo(**data[0])

        if battery.percentage < (self.threshold * 100):
            self.notify(battery)
            return True

        return False

    @classmethod
    def relevant_tag(cls) -> str:
        return "system.0.Batteries"

    @classmethod
    def required_data(cls) -> str:
        return "value"

    def notify(self, data):
        message = self.build_notifier_message(data)

        for notifier in self.notifiers:
            notifier.notify(message)

    def build_notifier_message(self, battery: BatteryInfo) -> NotificationMessage:

        def _generate_report(battery_info: BatteryInfo) -> NotificationMessage:
            """Generate a report to be sent via email"""
            mu = {
                "soc": "%",
                "power": "W",
                "current": "A",
                "voltage": "V",
            }

            title: str = t(
                "alerts.victron.battery_alert.title", threshold=self.threshold * 100
            )
            message: str = t("alerts.victron.battery_alert.message")

            d: dict[str, float] = battery_info.model_dump()

            translation_dict = {
                "soc": t("alerts.victron.battery_alert.soc"),
                "power": t("alerts.victron.battery_alert.power"),
                "current": t("alerts.victron.battery_alert.current"),
                "voltage": t("alerts.victron.battery_alert.voltage"),
            }

            for k, v in translation_dict.items():
                message = message + f"{v}: {round(d[k], 2)}{mu[k]}\n"

            return NotificationMessage(
                title=title,
                message=message,
            )

        return _generate_report(battery)
