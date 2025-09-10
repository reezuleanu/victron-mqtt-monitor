from victron_mqtt_monitor.alerts.base import BaseAlert
from victron_mqtt_monitor.interfaces import BatteryInfo


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

    def build_notifier_message(self, battery: BatteryInfo) -> str:

        def _generate_report(
            battery_info: BatteryInfo, language: str = "Romanian"
        ) -> str:
            """Generate a report to be sent via email"""
            mu = {
                "soc": "%",
                "power": "W",
                "current": "A",
                "voltage": "V",
            }
            # TODO maybe replace the dictionary iterating with string formatting
            match language:
                case "Romanian":
                    message = "Nivelul bateriilor a scazut sub {threshold}%!\n===Detalii baterii===\n\n"
                    translation_dict = {
                        "soc": "Procentaj",
                        "power": "Putere",
                        "current": "Curent",
                        "voltage": "Tensiune",
                    }
                case _:
                    raise Exception(f"Invalid report language: {language}")

            message = message.format(threshold=self.threshold * 100)
            d: dict[str, float] = battery_info.model_dump()

            for k, v in translation_dict.items():
                message = message + f"{v}: {round(d[k], 2)}{mu[k]}\n"

            return message

        return _generate_report(battery)
