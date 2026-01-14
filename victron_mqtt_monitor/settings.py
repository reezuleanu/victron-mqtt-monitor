from pydantic_settings import BaseSettings
from dotenv import load_dotenv

from victron_mqtt_monitor.constants import DEPLOYMENT_TYPES, LANGUAGE_OPTIONS

load_dotenv()


class Settings(BaseSettings):

    APP_NAME: str = ""

    DEPLOYMENT: DEPLOYMENT_TYPES = "prod"

    # victron mqtt settings
    VICTRON_ID: str
    BROKER_URL: str

    # email notifier settings
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_EMAIL: str
    SMTP_PASSWORD: str
    EMAIL_RECIPIENTS: list[str]

    LOCALE: LANGUAGE_OPTIONS = "en"


config = Settings()
