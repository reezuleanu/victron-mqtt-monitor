import time
import json
from typing import Callable

from loguru import logger
from paho.mqtt.client import MQTTMessage

from victron_mqtt_monitor.clients.mqtt_client import MQTTClient
from victron_mqtt_monitor.interfaces import VictronStats, BatteryInfo, Tree
from victron_mqtt_monitor.monitors.base import BaseMonitor
from victron_mqtt_monitor.alerts.base import BaseAlert
from victron_mqtt_monitor.utils import get_local_datetime


class VictronMonitor(BaseMonitor):
    def __init__(self, broker_url: str, victron_id: str, alerts: list[BaseAlert] = []):
        self._client = MQTTClient()
        self._client.on_message = self._build_callback()
        self.tree = Tree()
        self.broker_url: str = broker_url
        self.victron_id: str = victron_id
        self.alerts: list[BaseAlert] = alerts

    def run(self) -> None:
        rc = self._client.connect(self.broker_url, keepalive=50)
        if rc.value == 0:
            logger.info(f"Client connected to {self.broker_url} successfully")
        rc, _ = self._client.subscribe("N/#")
        if rc.value == 0:
            logger.info("Subscribed to topics successfully")

        try:
            while True:
                self._client.publish(f"R/{self.victron_id}/keepalive")
                self._client.loop_start()
                time.sleep(55)
                self._client.loop_stop()
        # except KeyboardInterrupt:
        #     # save tree
        #     with open("dev/tree.json", "w") as fp:
        #         json.dump(self.tree, fp, indent=2)
        except:
            self.run()  # Retry mechanism in case mqtt breaks somehow

    def _build_callback(self) -> Callable:

        def callback(client, userdata, flags: MQTTMessage, rc=None):

            decoded_message = json.loads(flags.payload.decode())
            self.tree.add_to_tree(flags.topic, decoded_message)

            if flags.topic == f"N/{self.victron_id}/system/0/Batteries":
                battery_stats = BatteryInfo(**decoded_message["value"][0])
                logger.info(battery_stats)
            local_time = get_local_datetime()

            # TODO move stupid time restriction, maybe implement libactions for this mess (never thought i'd say that)
            if local_time.hour > 9:
                self._check_alerts(flags.topic, decoded_message)

        return callback

    def _check_alerts(self, topic: str, decoded_message: dict) -> None:
        split_topics = topic.split("/")

        for alert in self.alerts:
            if alert.alerted:  # skip already notified alarms
                continue
            if not alert.relevant_tag() in ".".join(split_topics):
                continue

            # if the code gets to this point, the topic is relevant to the required data
            temp_tree = Tree()
            temp_tree.add_to_tree(topic, decoded_message)
            nested_path = f"{'.'.join(split_topics)}.{alert.required_data()}"

            # if the required data was also provided, check the alert
            if data := temp_tree.fetch_nested_value(nested_path):
                alert.alerted = alert.condition(data)
