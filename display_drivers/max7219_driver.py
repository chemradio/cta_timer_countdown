# Code is adapted from this author and under his license:
# Licence: GPLv3
# Copyright 2017 Paul Dwerryhouse <paul@dwerryhouse.com.au>

CHAR_MAP = {
    "0": 0x7E,
    "1": 0x30,
    "2": 0x6D,
    "3": 0x79,
    "4": 0x33,
    "5": 0x5B,
    "6": 0x5F,
    "7": 0x70,
    "8": 0x7F,
    "9": 0x7B,
    "a": 0x77,
    "b": 0x1F,
    "c": 0x4E,
    "d": 0x3D,
    "e": 0x4F,
    "f": 0x47,
    "g": 0x7B,
    "h": 0x37,
    "i": 0x30,
    "j": 0x3C,
    "k": 0x57,
    "l": 0x0E,
    "m": 0x54,
    "n": 0x15,
    "o": 0x1D,
    "p": 0x67,
    "q": 0x73,
    "r": 0x05,
    "s": 0x5B,
    "t": 0x0F,
    "u": 0x1C,
    "v": 0x3E,
    "w": 0x2A,
    "x": 0x37,
    "y": 0x3B,
    "z": 0x6D,
    "A": 0x77,
    "B": 0x1F,
    "C": 0x4E,
    "D": 0x3D,
    "E": 0x4F,
    "F": 0x47,
    "G": 0x7B,
    "H": 0x37,
    "I": 0x30,
    "J": 0x3C,
    "K": 0x57,
    "L": 0x0E,
    "M": 0x54,
    "N": 0x15,
    "O": 0x1D,
    "P": 0x67,
    "Q": 0x73,
    "R": 0x05,
    "S": 0x5B,
    "T": 0x0F,
    "U": 0x1C,
    "V": 0x3E,
    "W": 0x2A,
    "X": 0x37,
    "Y": 0x3B,
    "Z": 0x6D,
    " ": 0x00,
    "-": 0x01,
    "\xb0": 0x63,
    ".": 0x80,
}

REG_NO_OP = 0x00
REG_DIGIT_BASE = 0x01
REG_DECODE_MODE = 0x09
REG_INTENSITY = 0x0A
REG_SCAN_LIMIT = 0x0B
REG_SHUTDOWN = 0x0C
REG_DISPLAY_TEST = 0x0F


class Display:
    def __init__(self, spi, ss, intensity=7):
        self.spi = spi
        self.ss = ss
        self.buffer = bytearray(8)
        self.intensity = intensity
        self.reset()

    def reset(self):
        self.set_register(REG_DECODE_MODE, 0)
        self.set_register(REG_INTENSITY, self.intensity)
        self.set_register(REG_SCAN_LIMIT, 7)
        self.set_register(REG_DISPLAY_TEST, 0)
        self.set_register(REG_SHUTDOWN, 1)

    def set_register(self, register, value):
        self.ss.off()
        self.spi.write(bytearray([register, value]))
        self.ss.on()

    def decode_char(self, c):
        d = CHAR_MAP.get(c)
        return d if d != None else " "

    def write_to_buffer(self, s):
        l = len(s)
        if l < 8:
            s = "%-8s" % s
        for i in range(0, 8):
            self.buffer[7 - i] = self.decode_char(s[i])

    def write_to_buffer_with_dots(self, s):
        len_s = len(s)

        x = 0
        i = 0
        while i < len_s:
            if x >= 8:
                break

            elif i < (len_s - 1) and s[i + 1] == ".":
                self.buffer[7 - x] = self.decode_char(s[i]) | 0x80
                i += 1
            else:
                self.buffer[7 - x] = self.decode_char(s[i])

            x += 1
            i += 1

        while x < 8:
            self.buffer[7 - x] = self.decode_char(" ")
            x += 1

    def display(self):
        for i in range(0, 8):
            self.set_register(REG_DIGIT_BASE + i, self.buffer[i])

    def set_intensity(self, i):
        self.intensity = i
        self.set_register(REG_INTENSITY, self.intensity)
