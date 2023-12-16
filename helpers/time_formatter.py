import datetime

from enums.digit_display import DigitDisplay
from helpers.components import get_time_components_from_delta


def format_time(delta: datetime.timedelta, display_type: DigitDisplay):
    if display_type == DigitDisplay.EIGHT_DOTTED:
        return format_time_eight_digit_dotted(delta)
    elif display_type == DigitDisplay.SIX_DOTTED:
        return format_time_six_digit_dotted(delta)


def format_time_eight_digit_dotted(delta: datetime.timedelta) -> str:
    ...


def format_time_six_digit_dotted(delta: datetime.timedelta) -> str:
    if delta is None:
        return " . .IDLE. . "

    hours, minutes, seconds, microseconds = get_time_components_from_delta(delta)
    return "{:02d}.{:02d}.{:02d}".format(hours, minutes, seconds)

    # if hours > 0:
    #     return "{:02d}.{:02d}.{:02d}".format(hours, minutes, seconds)
    # else:
    #     if minutes > 0:
    #         return "{:02d}.{:02d}.{:02d}".format(
    #             minutes, seconds, int(str(microseconds)[:2])
    #         )
    #     else:
    #         return "{:02d}.{:04d}".format(seconds, int(str(microseconds)[:4]))
