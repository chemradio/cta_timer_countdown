import datetime


def get_time_components_from_delta(delta: datetime.timedelta):
    """
    Get hours, minutes, seconds, and microseconds from a timedelta.

    Parameters:
    - delta (timedelta): The timedelta object.

    Returns:
    - hours (int): The number of hours.
    - minutes (int): The number of minutes.
    - seconds (int): The number of seconds.
    - microseconds (int): The number of microseconds.
    """
    total_seconds = delta.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    microseconds = int(delta.microseconds)

    return hours, minutes, seconds, microseconds
