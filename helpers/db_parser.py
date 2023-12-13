import datetime
import json
from pathlib import Path


def parse_database(db_path: Path | str) -> list[dict]:
    with open(db_path, "rt") as f:
        raw_data: list[dict] = json.load(f)

    for program in raw_data:
        if not program["start"]:
            raw_data.remove(program)

        program_start = datetime.time.fromisoformat(program["start"])
        print(program_start)

        if not program["duration"] and not program["end"]:
            raw_data.remove(program)

        if program["end"] and program["duration"]:
            program.pop("duration")
        else:
            duration = program.pop("duration")
            program["end"]
