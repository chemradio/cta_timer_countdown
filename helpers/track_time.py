import datetime

from enums.timer_status import TimerStatus
from helpers.get_now_tz import construct_now_datetime, get_target_tz


def track_time(
    current_datetime: datetime.datetime = construct_now_datetime(),
    db: list[dict] = list(),
) -> tuple[TimerStatus, datetime.timedelta | None]:
    print(current_datetime)
    if not db:
        return TimerStatus.IDLE, None

    current_time = current_datetime.time()

    for program in db:
        if current_datetime.weekday() not in program["weekdays"]:
            continue

        if current_time >= program["end"]:
            continue

        if current_time < program["start"]:
            program_start_datetime = datetime.datetime.combine(
                datetime.date.today(), program["start"], get_target_tz()
            )
            diff = program_start_datetime - current_datetime
            return TimerStatus.COUNTDOWN, diff

        elif current_time >= program["start"]:
            program_end_datetime = datetime.datetime.combine(
                datetime.date.today(), program["end"], get_target_tz()
            )
            diff = program_end_datetime - current_datetime
            return TimerStatus.ONAIR, diff

    else:
        for program in db:
            today_weekday = current_datetime.weekday()
            tomorrow_weekday = 0 if today_weekday == 6 else today_weekday + 1
            if tomorrow_weekday in program["weekdays"]:
                tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                tomorrow_start_datetime = datetime.datetime.combine(
                    tomorrow, program["start"], get_target_tz()
                )
                diff = tomorrow_start_datetime - current_datetime
                return TimerStatus.COUNTDOWN_TOMORROW, diff

        return TimerStatus.IDLE, None
