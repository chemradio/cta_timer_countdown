import time

from display_drivers.abstract_display import PrintableDigitDisplay
from helpers.time_formatter import format_time
from helpers.track_time import track_time


def print_time_to_display(db: list[dict], display: PrintableDigitDisplay) -> None:
    while True:
        # construct closest time object (optional, may be None)
        timer_status, timedelta_obj = track_time(db=db)
        print(f"{timer_status=}, {timedelta_obj=}")

        # format time to display
        formatted_time = format_time(timedelta_obj, display.display_type)
        print(f"{formatted_time=}")

        display.print_to_display(formatted_time)
        time.sleep(1 - time.time() % 1)
