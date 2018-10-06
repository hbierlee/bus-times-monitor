import time
import datetime

from schedule import read_schedule
from services import get_services_for_schedule, is_service_available_for_date


def get_time_as_string(datetime=datetime.datetime.now()):
    return datetime.strftime("%H:%M:00")  # TODO maybe remove 00?


def start_bus_pole():
    schedule = read_schedule()
    services = get_services_for_schedule(schedule)

    while True:
        index_of_next_departing_bus = find_index_of_next_departing_bus(
            schedule, services)
        print(index_of_next_departing_bus)
        print(schedule[index_of_next_departing_bus])

        bus = schedule[index_of_next_departing_bus]
        departure_time = time_string_to_date(bus["departure_time"])
        from_now = time_from_now(departure_time)
        print("The next bus ({} to {}) leaves in {} minute(s) from now.".format(
            bus["route_short_name"], bus["trip_headsign"], from_now))
        time.sleep(30)


def time_string_to_date(time_string):
    return datetime.time(*map(int, time_string.split(":")))


def time_from_now(time):
    return (datetime.datetime.combine(datetime.date.today(), time) - datetime.datetime.now()).seconds / 60


# datetime.time().strftime(..)
def find_index_of_next_departing_bus(schedule, services, datetime=datetime.datetime.now()):
    index = -1
    time_string = get_time_as_string(datetime)
    for index, bus in enumerate(schedule):
        if bus["departure_time"] >= time_string and is_service_available_for_date(bus["service_id"], services, datetime.date()):

            return index

    print("no bus found")


start_bus_pole()
