from enum import Enum


class TimerStatus(Enum):
    IDLE = "IDLE"
    ONAIR = "ONAIR"
    COUNTDOWN = "COUNTDOWN"
    COUNTDOWN_TOMORROW = "COUNTDOWN_TOMORROW"
