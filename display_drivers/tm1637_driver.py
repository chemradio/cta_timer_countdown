from datetime import datetime, timedelta
from time import sleep, time

import wiringpi
from wiringpi import GPIO

from display_drivers.abstract_display import PrintableDigitDisplay
from enums.digit_display import DigitDisplay

TM1637_CMD1 = 64  # 0x40 data command
TM1637_CMD2 = 192  # 0xC0 address command
TM1637_CMD3 = 128  # 0x80 display control command
TM1637_DSP_ON = 8  # 0x08 display on
TM1637_DELAY = 0.01  # 10us delay between clk/dio pulses
TM1637_DELAY = 10e-6  # 10us delay between clk/dio pulses
TM1637_MSB = 128  # msb is the decimal point or the colon depending on your display

_SEGMENTS = bytearray(
    b"\x3F\x06\x5B\x4F\x66\x6D\x7D\x07\x7F\x6F\x77\x7C\x39\x5E\x79\x71\x3D\x76\x06\x1E\x76\x38\x55\x54\x3F\x73\x67\x50\x6D\x78\x3E\x1C\x2A\x76\x6E\x5B\x00\x40\x63"
)


class TM1637(PrintableDigitDisplay):
    """Library for quad 7-segment LED modules based on the TM1637 LED driver."""

    def __init__(self, clk, dio, brightness=7, power_pin: int = 9):
        self.clk = clk
        self.dio = dio
        self.display_type = DigitDisplay.SIX_DOTTED
        if not 0 <= brightness <= 7:
            raise ValueError("Brightness out of range")
        self._brightness = brightness

        wiringpi.wiringPiSetup()
        wiringpi.pinMode(self.clk, GPIO.OUTPUT)
        wiringpi.pinMode(self.dio, GPIO.OUTPUT)
        wiringpi.pinMode(power_pin, GPIO.OUTPUT)
        wiringpi.digitalWrite(power_pin, GPIO.HIGH)

        sleep(TM1637_DELAY)

        self._write_data_cmd()
        self._write_dsp_ctrl()

    def _start(self):
        wiringpi.digitalWrite(self.dio, GPIO.LOW)
        sleep(TM1637_DELAY)
        wiringpi.digitalWrite(self.clk, GPIO.LOW)
        sleep(TM1637_DELAY)

    def _stop(self):
        wiringpi.digitalWrite(self.dio, GPIO.LOW)
        sleep(TM1637_DELAY)
        wiringpi.digitalWrite(self.clk, GPIO.HIGH)
        sleep(TM1637_DELAY)
        wiringpi.digitalWrite(self.dio, GPIO.HIGH)

    def _write_data_cmd(self):
        self._start()
        self._write_byte(TM1637_CMD1)
        self._stop()

    def _write_dsp_ctrl(self):
        self._start()
        self._write_byte(TM1637_CMD3 | TM1637_DSP_ON | self._brightness)
        self._stop()

    def _write_byte(self, b):
        for i in range(8):
            wiringpi.digitalWrite(self.dio, (b >> i) & 1)
            sleep(TM1637_DELAY)
            wiringpi.digitalWrite(self.clk, GPIO.HIGH)
            sleep(TM1637_DELAY)
            wiringpi.digitalWrite(self.clk, GPIO.LOW)
            sleep(TM1637_DELAY)
        wiringpi.digitalWrite(self.clk, GPIO.LOW)
        sleep(TM1637_DELAY)
        wiringpi.digitalWrite(self.clk, GPIO.HIGH)
        sleep(TM1637_DELAY)
        wiringpi.digitalWrite(self.clk, GPIO.LOW)
        sleep(TM1637_DELAY)

    def brightness(self, val=None):
        if val is None:
            return self._brightness
        if not 0 <= val <= 7:
            raise ValueError("Brightness out of range")

        self._brightness = val
        self._write_data_cmd()
        self._write_dsp_ctrl()

    def write(self, segments, pos=0):
        if not 0 <= pos <= 5:
            raise ValueError("Position out of range")
        self._write_data_cmd()
        self._start()
        self._write_byte(TM1637_CMD2 | pos)

        for i in [2, 1, 0, 5, 4, 3]:
            self._write_byte(segments[i])

        self._stop()
        self._write_dsp_ctrl()

    def encode_string(self, string):
        """Convert a string to LED segments.

        Convert an up to 6 character length string containing 0-9, a-z,
        space, dash, star and '.' to an array of segments, matching the length of
        the source string."""
        segments = bytearray(len(string))
        j = 0
        for i in range(len(string)):
            if string[i] == "." and j > 0:
                segments[j - 1] |= TM1637_MSB
                continue
            segments[j] = self.encode_char(string[i])
            j += 1
        return segments

    def encode_char(self, char):
        """Convert a character 0-9, a-z, space, dash or star to a segment."""
        o = ord(char)
        if o == 32:
            return _SEGMENTS[36]  # space
        if o == 42:
            return _SEGMENTS[38]  # star/degrees
        if o == 45:
            return _SEGMENTS[37]  # dash
        if o >= 65 and o <= 90:
            return _SEGMENTS[o - 55]  # uppercase A-Z
        if o >= 97 and o <= 122:
            return _SEGMENTS[o - 87]  # lowercase a-z
        if o >= 48 and o <= 57:
            return _SEGMENTS[o - 48]  # 0-9
        raise ValueError("Character out of range: {:d} '{:s}'".format(o, char))

    def print_to_display(self, input: str) -> None:
        encoded_string = self.encode_string(input)
        self.write(encoded_string)


# def display_current_time(tm1637):
#     utc_offset = timedelta(hours=6)

#     while True:
#         # Get the current UTC time
#         current_time_utc = datetime.utcnow().time()

#         # Add the UTC offset to get the desired time zone (UTC+6)
#         current_time_desired_tz = (
#             datetime.combine(datetime.today(), current_time_utc) + utc_offset
#         )

#         # Format the time as a string (HHMMSS)
#         time_str = "{:02d}.{:02d}.{:02d}".format(
#             current_time_desired_tz.hour,
#             current_time_desired_tz.minute,
#             current_time_desired_tz.second,
#         )

#         # Write the segments to the display
#         tm1637.print_to_display(time_str)

#         # Wait for one second before updating again
#         sleep(1 - time() % 1)  # Adjust for the time taken by the operations above
