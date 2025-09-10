from victron_mqtt_monitor.utils import init_logger
from victron_mqtt_monitor.settings import config
from victron_mqtt_monitor.monitors.victron_monitor import VictronMonitor
from victron_mqtt_monitor.alerts.victron import BatteryAlert

init_logger(config.DEPLOYMENT, config.APP_NAME)


monitor = VictronMonitor(
    config.BROKER_URL, config.VICTRON_ID, alerts=[BatteryAlert(0.85)]
)

monitor.run()
