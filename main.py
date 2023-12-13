import datetime

from helpers.db_parser import parse_database

db = parse_database("./program_starts.json")

current_datetime = datetime.datetime.utcnow() + datetime.timedelta(hours=6)

# for program in db:
#     if current_datetime.weekday not in program["weekdays"]:
#         continue

x = current_datetime.time()
y = datetime.time(hour=23, minute=59)
print(x > y)
