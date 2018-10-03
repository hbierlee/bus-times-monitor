import os.path
import csv
import time
import operator 

UPPSALA_POLACKSBACKEN_STOP_ID = "740012548"

DATA_PATH = os.path.join("../data/")
STOP_TIMES_PATH = os.path.join(DATA_PATH, "original/stop_times.txt")
TRIPS_PATH = os.path.join(DATA_PATH, "original/trips.txt")
ROUTES_PATH = os.path.join(DATA_PATH, "original/routes.txt")

SCHEDULE_DESTINATION_PATH = os.path.join(DATA_PATH, "schedules/schedule-" + str(time.time()) + ".txt")
SCHEDULE_FIELDNAMES = ["trip_id","arrival_time","departure_time","stop_id","stop_sequence","pickup_type","drop_off_type", "route_id", "trip_headsign"]

def write_csv_file(destination, fieldnames, rows):
	with open(destination, 'w') as file:
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(rows)

def sub_dict(somedict, somekeys, default=None):
	return dict([ (k, somedict.get(k, default)) for k in somekeys ])

def get_stop_times_for_stop_id(stop_id, stop_times_path=STOP_TIMES_PATH):
	print('get_stop_times_for_stop_id=' + UPPSALA_POLACKSBACKEN_STOP_ID)
	with open(stop_times_path, 'rb') as csvfile:
		stop_times = csv.DictReader(csvfile, delimiter=',')
		return filter(lambda row: row['stop_id'] == stop_id, stop_times)

def append_trip_fields_to_schedule(schedule, trips_path=TRIPS_PATH):
	with open(trips_path) as trips_file:
		trips = csv.DictReader(trips_file)
		sorting_key = operator.itemgetter("trip_id")
		schedule = sorted(schedule, key=sorting_key)  # should already be the case
		trips = sorted(trips, key=sorting_key)
		for bus, trip in zip(schedule, trips):
			bus.update(trip)
		return schedule
		

def append_route_fields_to_schedule(schedule, routes_path=ROUTES_PATH):
	with open(routes_path) as routes_file:
		routes = csv.DictReader(routes_file)
		sorting_key = operator.itemgetter("route_id")
		schedule = sorted(schedule, key=sorting_key)
		routes = sorted(routes, key=sorting_key)  # should already be the case
		for bus, route in zip(schedule, routes):
			bus.update(route)
		return schedule


def create_schedule(stop_id):
	print('get_stop_times_for_stop_id')
	schedule = get_stop_times_for_stop_id(stop_id)
	append_trip_fields_to_schedule(schedule)
	print("append_trip_fields_to_schedule")
	append_route_fields_to_schedule(schedule)
	print("append_route_fields_to_schedule")
	print(schedule)
	write_csv_file(SCHEDULE_DESTINATION_PATH, schedule[0].keys(), schedule)

create_schedule(UPPSALA_POLACKSBACKEN_STOP_ID)




