import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion, MQTTProtocolVersion


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
