import time
import datetime

from schedule import read_schedule
from service import get_services_for_schedule, is_service_available_for_date


def get_time_as_string(datetime):
    return datetime.strftime("%H:%M:00")


def get_some_time_ranges(start=8, to=16):
    r = []
    for hour in range(start, to):
        for minute in range(0, 59):
            r.append(datetime.datetime.combine(
                datetime.date.today(), datetime.time(hour, minute)))
    return r


def start_bus_pole():
    schedule = read_schedule()
    services = get_services_for_schedule(schedule)

    time_ranges = get_some_time_ranges()

    # for time in time_ranges:
    while True:
        index_of_next_departing_bus = find_index_of_next_departing_bus(
            schedule, services,
        )

        bus = schedule[index_of_next_departing_bus]
        departure_time = time_string_to_date(bus["departure_time"])
        from_now = minutes_from_now(departure_time)
        from_now = 0 if (from_now == 1439) else from_now

        print("[{}] The next bus ({} to {}) leaves in {} minute(s) from now (trip_id: {})".format(
            datetime.datetime.now(), bus["route_short_name"], bus["trip_headsign"], from_now, bus["trip_id"]))

        time.sleep(60) # TODO trigger this instead by using the clock minute (AKA use cron)


def time_string_to_date(time_string):
    return datetime.time(*map(int, time_string.split(":")))


def minutes_from_now(time):
    return (datetime.datetime.combine(datetime.date.today(), time) - datetime.datetime.now()).seconds // 60


def find_index_of_next_departing_bus(schedule, services, now=None):
    if now is None:
        now = datetime.datetime.now().replace(second=0)

    index = -1
    time_string = get_time_as_string(now)
    for index, bus in enumerate(schedule):
        if bus["departure_time"] >= time_string and is_service_available_for_date(bus["service_id"], services, now.date()):
            return index

    print("no bus found")


start_bus_pole()
