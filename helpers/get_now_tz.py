import datetime


def construct_now_datetime() -> datetime.datetime:
    offset_hours = 6
    target_timezone = datetime.timezone(datetime.timedelta(hours=offset_hours))
    return datetime.datetime.now(target_timezone)
