import datetime
from typing import List

__DATE_FORMAT_ISO8601: str = '%Y-%m-%dT%H:%M:%S'


def get_current_iso_timestamp() -> str:
    """Get current ISO-8601 timestamp

    Returns:
        str: The timestamp
    """
    return datetime.datetime.now().strftime(__DATE_FORMAT_ISO8601)


__DATE_FORMAT_ISO8601_3f_colon_z: str = '%Y-%m-%dT%H:%M:%S._%f_%z'


def get_current_iso_timestamp_p3f_pcz(tz: datetime._TzInfo = None) -> str:
    """
    Returns the current date and time in ISO 8601 format with millisecond precision,
    colon separator for hours, minutes, and seconds, and UTC or local timezone offset.

    Args:
        tz (datetime._TzInfo): Optional timezone object. If not provided, the function will use the system's default timezone.

    Returns:
        str: The current date and time in ISO 8601 format.
    """
    date_list: List[str] = datetime.datetime.now(tz=tz).strftime(__DATE_FORMAT_ISO8601_3f_colon_z).split('_')
    f: str = date_list[1]
    if f:
        f = '%3.3s' % f
    else:
        f = '000'
    z: str = date_list[2]
    if z:
        z = '%s:%s' % (z[:3], z[3:])
    else:
        z = 'Z'
    return '%s%s%s' % (date_list[0], f, z)
