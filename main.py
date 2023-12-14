from display_drivers.tm1637_driver import TM1637
from helpers.db_parser import parse_database
from helpers.display_printer import print_time_to_display


def main():
    # create displays
    displays = {
        "time_display": TM1637(clk=9, dio=10, power_pin=4),
        "aux_display": None,
    }

    # parse database
    db = parse_database("./program_starts.json")

    print_time_to_display(db, displays["time_display"])


if __name__ == "__main__":
    main()
