import time
import datetime

from schedule import init_schedule_by_quadrant
from service import get_services_for_schedule, is_service_available_for_date


def get_time_as_string(datetime):
    return datetime.strftime("%H:%M:00")


def start_bus_pole():
    schedule_by_quadrant = init_schedule_by_quadrant()
    services_by_quadrant = {quadrant: get_services_for_schedule(
        schedule) for quadrant, schedule in schedule_by_quadrant.items()}

    while True:
        value_by_quadrant = {quadrant: find_next_departing_bus(
            schedule, services_by_quadrant[quadrant]) for quadrant, schedule in schedule_by_quadrant.items()}

        print(value_by_quadrant)

        try:
            from display import display
            display(value_by_quadrant["A"], value_by_quadrant["B"],
                    value_by_quadrant["C"], value_by_quadrant["D"])
        except ImportError:
            print('SenseHAT module not found, not displaying.')



        # print("[{}] The next bus ({} to {}) leaves in {} minute(s) from now (trip_id: {})".format(
        #     datetime.datetime.now(), bus["route_short_name"], bus["trip_headsign"], from_now, bus["trip_id"]))

        # TODO trigger this instead by using the clock minute (AKA use cron)
        time.sleep(60)


def find_next_departing_bus(schedule, services):
    index = find_index_of_next_departing_bus(schedule, services)
    if index is -1:
        return 0
    
    bus = schedule[index]
    departure_time = time_string_to_date(bus["departure_time"])
    from_now = minutes_from_now(departure_time)
    from_now = 0 if (from_now == 1439) else from_now
    from_now = from_now + 1
    return from_now


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

    # If all buses have gone for this day, find first available morning bus
    for index, bus in enumerate(schedule):
        if is_service_available_for_date(bus["service_id"], services, now.date()):
            return index
        
    # No bus found, disable quadrant
    return -1


start_bus_pole()
