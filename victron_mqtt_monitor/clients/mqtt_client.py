import json

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion, MQTTProtocolVersion
from loguru import logger

from victron_mqtt_monitor.settings import config
from victron_mqtt_monitor.interfaces import Tree, VictronStats, BatteryInfo
from victron_mqtt_monitor.notifiers.email_notifier import EmailNotifier
from victron_mqtt_monitor.utils import get_local_datetime

tree = Tree()
alerted = False


def _generate_report(battery_info: BatteryInfo, language: str = "Romanian") -> str:
    """Generate a report to be sent via email"""
    mu = {
        "soc": "%",
        "power": "W",
        "current": "A",
        "voltage": "V",
    }
    match language:
        case "Romanian":
            message = "Nivelul bateriilor a scazut sub 85%!\n===Detalii baterii===\n\n"
            translation_dict = {
                "soc": "Procentaj",
                "power": "Putere",
                "current": "Curent",
                "voltage": "Tensiune",
            }
        case _:
            raise Exception(f"Invalid report language: {language}")

    d: dict[str, float] = battery_info.model_dump()

    for k, v in translation_dict.items():
        message = message + f"{v}: {round(d[k], 2)}{mu[k]}\n"

    return message


def callback(client, userdata, flags: mqtt.MQTTMessage, rc=None):
    global alerted

    decoded_message = json.loads(flags.payload.decode())
    tree.add_to_tree(flags.topic, decoded_message)

    if flags.topic == f"N/{config.VICTRON_ID}/system/0/Batteries":
        battery_stats = BatteryInfo(**decoded_message["value"][0])
        logger.info(battery_stats)
        # stats = VictronStats(**tree["N"][config.VICTRON_ID]["system"]["0"])
        # logger.info(stats.Batteries[0])

        # TODO fix this, this is horrible
        local_time = get_local_datetime()
        if (
            battery_stats.percentage < 85
            and local_time.hour > 9
            and local_time.hour < 0
        ):
            if alerted:
                return
            EmailNotifier.notify(_generate_report(battery_stats))
            alerted = True


class MQTTClient(mqtt.Client):
    def __init__(
        self,
        callback_api_version=CallbackAPIVersion.VERSION1,
        client_id="",
        clean_session=None,
        userdata=None,
        protocol=MQTTProtocolVersion.MQTTv311,
        transport="tcp",
        reconnect_on_failure=True,
        manual_ack=False,
    ):
        super().__init__(
            callback_api_version,
            client_id,
            clean_session,
            userdata,
            protocol,
            transport,
            reconnect_on_failure,
            manual_ack,
        )
        self.on_message = callback
        self.tree = tree
