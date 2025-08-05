from datetime import datetime, timezone
from tzlocal import get_localzone


def get_local_datetime() -> datetime:
    return datetime.now(get_localzone())
