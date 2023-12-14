import datetime


def construct_now_datetime() -> datetime.datetime:
    return datetime.datetime.now(get_target_tz())
    # return datetime.datetime.now()


def get_target_tz() -> datetime.timezone:
    offset_hours = 6
    return datetime.timezone(datetime.timedelta(hours=offset_hours))
