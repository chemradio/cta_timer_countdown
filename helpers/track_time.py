import datetime

from helpers.get_now_tz import construct_now_datetime


def track_time(
    current_datetime: datetime.datetime = construct_now_datetime(),
    db: list[dict] = list(),
) -> datetime.time | None:
    if not db:
        return None

    # check if today any programs going on air
    weekdays_with_programs = list()
    for program in db:
        weekdays_with_programs.extend(program["weekdays"])
    weekdays_with_programs = set(weekdays_with_programs)

    if current_datetime.weekday not in weekdays_with_programs:
        return None

    # find time / most logic
    ...

    return datetime.time(...)
