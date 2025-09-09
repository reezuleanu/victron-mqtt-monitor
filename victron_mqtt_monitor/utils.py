from datetime import datetime
from sys import stdout
import json

from tzlocal import get_localzone
from loguru import logger

from victron_mqtt_monitor.settings import DEPLOYMENT_TYPES


def get_local_datetime() -> datetime:
    return datetime.now(get_localzone())


def init_logger(deployment_type: DEPLOYMENT_TYPES) -> None:
    """Initialize the loguru logger based on the deployment type"""

    logger.remove()

    match deployment_type:
        case DEPLOYMENT_TYPES.PROD:

            def json_sink(message):
                record = message.record
                json_record = {
                    "time": record["time"].isoformat(),
                    "level": record["level"].name,  # flatten the dict
                    "name": record["name"],
                    "function": record["function"],
                    # "line": record["line"],
                    "message": record["message"],
                    "extra": record["extra"],
                }
                print(json.dumps(json_record), file=stdout)

            logger.add(json_sink)

        case DEPLOYMENT_TYPES.DEV:

            def dev_formatting(message) -> str:
                format = f"<cyan>[{{time}}][{{level}}][{{name}}][{{function}}]</cyan> {{message}}"
                if message.get("extra"):
                    format += " <yellow>[{extra}]</yellow>"
                format += "\n"
                return format

            logger.add(stdout, colorize=True, format=dev_formatting)

        case _:
            raise Exception(f"Invalid deployment type: '{deployment_type}'")
            exit(1)

    logger.info("Logger initialized successfully")
