import datetime
import json
from pathlib import Path


def parse_database(db_path: Path | str) -> list[dict]:
    with open(db_path, "rt") as f:
        database: list[dict] = json.load(f)

    for program in database:
        if not program.get("start"):
            raise ValueError(f"Program {program.get('name')} has no start time.")
            # raw_data.remove(program)

        program_start = datetime.time.fromisoformat(program["start"])
        program["start"] = program_start

        if not program.get("duration") and not program.get("end"):
            raise ValueError(
                f"Can't determine end time for program {program.get('name')}."
            )
            # raw_data.remove(program)

        if program.get("duration"):
            start_datetime = datetime.datetime.combine(
                datetime.datetime(year=2023, month=1, day=1), program_start
            )

            duration = program.pop("duration")
            duration_delta = parse_iso_to_delta(duration)
            program_end_datetime = start_datetime + duration_delta

            program_end = program_end_datetime.time()

        elif program.get("end"):
            program_end = datetime.time.fromisoformat(program["end"])
            if program_end <= program_start:
                raise ValueError(
                    f"Program {program.get('name')} end time is earlier than it's start."
                )
        program["end"] = program_end

    return database


def parse_iso_to_delta(iso_time: str) -> datetime.timedelta:
    hours, minutes, seconds = 0, 0, 0
    time_array = iso_time.split(":")
    if len(time_array) < 2:
        raise ValueError("Wrong iso timestring. Less than two colon-separated values")
    minutes = int(time_array[-2])
    seconds = int(time_array[-1])
    if len(time_array) > 2:
        hours = int(time_array[-3])

    return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
