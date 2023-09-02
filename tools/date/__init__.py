import datetime

__DATE_FORMAT_ISO8601: str = '%Y-%m-%dT%H:%M:%S'


def get_current_iso_timestamp() -> str:
    """Get current ISO-8601 timestamp

    Returns:
        str: The timestamp
    """
    return datetime.date.today().strftime(__DATE_FORMAT_ISO8601)
