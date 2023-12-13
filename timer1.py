import datetime

from enums.digit_display import DigitDisplay

from helpers.time_formatter import format_eight_digit_dotted, format_six_digit_dotted

program_starts = [
    datetime.time(hour=2, minute=24, second=0),
    datetime.time(hour=18, minute=0, second=4),
    datetime.time(hour=14, minute=0, second=0),
]


def global_timer(program_starts: list[datetime.time] = []) -> str:
    tz_offset = datetime.timedelta(hours=6)
    current_datetime = datetime.datetime.utcnow() + tz_offset

    if current_datetime.weekday() in (5, 6):
        return ""

    closest_time = min(
        program_starts,
        key=lambda x: abs(
            datetime.datetime.combine(datetime.date.today(), x) - current_datetime
        ).total_seconds(),
    )
    print(f"{closest_time=}")
    print(f"{current_datetime.time()=}")
    return single_timer(current_datetime, closest_time)


def single_timer(
    current_datetime: datetime.datetime,
    program_start: datetime.time,
    display_type: DigitDisplay = DigitDisplay.SIX_DOTTED,
):
    # Calculate the time remaining until the closest time
    program_datetime = datetime.datetime.combine(datetime.date.today(), program_start)
    time_remaining = program_datetime - current_datetime

    if display_type == DigitDisplay.SIX_DOTTED:
        return format_six_digit_dotted(time_remaining)
    elif display_type == DigitDisplay.EIGHT_DOTTED:
        return format_eight_digit_dotted(time_remaining)


print(global_timer(program_starts))
