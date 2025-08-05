import time
import json

from victron_mqtt_monitor.settings import config
from victron_mqtt_monitor.clients.mqtt_client import MQTTClient


client = MQTTClient()

rc = client.connect(config.BROKER_URL, keepalive=50)
if rc.value == 0:
    print(f"Client connected to {config.BROKER_URL} successfully")
rc, _ = client.subscribe("N/#")
if rc.value == 0:
    print("Subscribed to topics successfully")


try:
    while True:
        client.publish(f"R/{config.VICTRON_ID}/keepalive")
        client.loop_start()
        time.sleep(55)
        client.loop_stop()
except KeyboardInterrupt:
    # save tree
    with open("dev/tree.json", "w") as fp:
        json.dump(client.tree, fp, indent=2)
