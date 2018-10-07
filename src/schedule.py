import os
import os.path
import csv
import time
import operator

UPPSALA_POLACKSBACKEN_STOP_ID = "740012548"

DATA_PATH = os.path.join(os.path.dirname(__file__), '../data')
STOP_TIMES_PATH = os.path.join(DATA_PATH, "stop_times.txt")
TRIPS_PATH = os.path.join(DATA_PATH, "trips.txt")
ROUTES_PATH = os.path.join(DATA_PATH, "routes.txt")
CALENDAR_PATH = os.path.join(DATA_PATH, "calendar.txt")
CALENDAR_DATES_PATH = os.path.join(DATA_PATH, "calendar_dates.txt")
TIMEZONE = "Europe/Stockholm"

SCHEDULES_FOLDER_PATH = os.path.join(DATA_PATH, "schedules/")
SCHEDULE_FIELDNAMES = [
    "trip_id",
    "route_id",
    "service_id",
    "route_short_name",
    "trip_headsign",
    "departure_time",
]


def get_schedule_filename(): return "schedule-" + str(int(time.time())) + ".csv"

def write_csv_file(destination, fieldnames, rows):
    with open(destination, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def sub_dict(somedict, somekeys, default=None):
    return dict([(k, somedict.get(k, default)) for k in somekeys])


def get_stop_times_for_stop_id(stop_id, stop_times_path=STOP_TIMES_PATH):
    with open(stop_times_path, 'rb') as csvfile:
        stop_times = csv.DictReader(csvfile, delimiter=',')
        return filter(lambda row: row['stop_id'] == stop_id, stop_times)


def inner_join_file_to_schedule(schedule, path, key):
    with open(path) as file:
        other_data = csv.DictReader(file)

        sorting_key = operator.itemgetter(key)
        schedule = sorted(schedule, key=sorting_key)
        other_data = sorted(other_data, key=sorting_key)

        # TODO can be improved by just using zip from the index of the first trip_id match (I think?)
        otherIndex = 0
        for bus in schedule:
            routeEntry = next({"other": other, "index": index} for index, other in enumerate(
                other_data[otherIndex+1:]) if other[key] == bus[key])
            otherIndex = routeEntry["index"]
            bus.update(routeEntry["other"])
        return schedule

def create_schedule(stop_id=UPPSALA_POLACKSBACKEN_STOP_ID):
    # read and join data
    print("create_schedule")
    schedule = get_stop_times_for_stop_id(stop_id)
    inner_join_file_to_schedule(schedule, TRIPS_PATH, "trip_id")
    inner_join_file_to_schedule(schedule, ROUTES_PATH, "route_id")

    # clean and sort data
    schedule = map(lambda bus: sub_dict(bus, SCHEDULE_FIELDNAMES), schedule)
    for bus in schedule:  # add zero padding to hours
        if len(bus["departure_time"].split(":")[0]) == 1:
            bus["departure_time"] = "0" + bus["departure_time"]

    schedule = sorted(schedule, key=operator.itemgetter("departure_time"))

    return schedule

def read_schedule(path=SCHEDULES_FOLDER_PATH):
    with open(os.path.join(path, "schedule-1538856523.csv")) as file: # TODO get latest schedule
        schedule = csv.DictReader(file, delimiter=',')
        return list(schedule)



# schedule = create_schedule()
# write_csv_file(os.path.join(SCHEDULES_FOLDER_PATH, get_schedule_filename()), SCHEDULE_FIELDNAMES, schedule)
# schedule = read_schedule()

# read_calendar_dates_for_service_ids(map(lambda bus: bus["service_id"], schedule))

# TODO rename file to schedule.py
# TODO rename bus vars to trip ?
# TODO old, probably remove
# def time_string_to_date(time_string): 
#     time_string = map(int, time_string.split(":"))
#     while (time_string[0] > 23): time_string[0] = time_string[0] - 24 remove
#     return datetime.time(*time_string)

# TODO maybe remove
# import datetime
# def time_string_to_date(time_string): return datetime.time(*map(int, time_string.split(":")))
# def sort_schedule_by_departure_time(schedule): return sorted(schedule, key=lambda bus: time_string_to_date(bus["departure_time"]))
