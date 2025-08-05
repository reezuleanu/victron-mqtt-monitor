from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # victron mqtt settings
    VICTRON_ID: str
    BROKER_URL: str

    # email notifier settings
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_EMAIL: str
    SMTP_PASSWORD: str
    EMAIL_RECIPIENTS: list[str]


config = Settings()
