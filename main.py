from helpers.db_parser import parse_database
from helpers.track_time import track_time


def main():
    # parse database
    db = parse_database("./program_starts.json")

    # construct closest time object (optional, may be None)
    timer_status, timedelta_obj = track_time(db=db)

    # format time to display
    ...

    # write string to display
    ...


if __name__ == "__main__":
    main()
