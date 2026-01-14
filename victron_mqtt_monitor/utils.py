from datetime import datetime
from sys import stdout
import json

from tzlocal import get_localzone
from loguru import logger
import i18n

from victron_mqtt_monitor.constants import LANGUAGE_OPTIONS
from victron_mqtt_monitor.settings import DEPLOYMENT_TYPES


def get_local_datetime() -> datetime:
    return datetime.now(get_localzone())


def init_logger(deployment_type: DEPLOYMENT_TYPES, app_name: str) -> None:
    """Initialize the loguru logger based on the deployment type"""

    logger.remove()

    match deployment_type:
        case DEPLOYMENT_TYPES.PROD:

            def json_sink(message):
                record = message.record
                json_record = {
                    "app_name": app_name,
                    "time": record["time"].isoformat(),
                    "level": record["level"].name,
                    "name": record["name"],
                    "function": record["function"],
                    "message": record["message"],
                    "extra": record["extra"],
                }
                print(json.dumps(json_record), file=stdout)

            logger.add(json_sink)

        case DEPLOYMENT_TYPES.DEV:

            def dev_formatting(message) -> str:
                format = f"<cyan>{f'[{app_name}]' if app_name else ''}[{{time}}][{{level}}][{{name}}][{{function}}]</cyan> {{message}}"
                if message.get("extra"):
                    format += " <yellow>[{extra}]</yellow>"
                format += "\n"
                return format

            logger.add(stdout, colorize=True, format=dev_formatting)

        case _:
            raise Exception(f"Invalid deployment type: '{deployment_type}'")
            exit(1)

    logger.info("Logger initialized successfully")


def init_i18n(language: LANGUAGE_OPTIONS = "en"):
    try:
        settings = {
            "locale": str(language),
            "load_path": ["victron_mqtt_monitor/localization/packs"],
            "filename_format": "{locale}.{format}",
            "file_format": "yaml",
            "enable_memoization": True,
        }

        for k, v in settings.items():
            i18n.set(k, v)

        logger.info("i18n initialized successfully")
        logger.info(f"i18n set locale: {i18n.get('locale')}")
    except Exception as e:
        logger.exception(f"Could not initialize i18n, reason: {str(e)}")
