import os.path
import csv
import time
import operator 

UPPSALA_POLACKSBACKEN_STOP_ID = "740012548"

DATA_PATH = os.path.join("../data/")
STOP_TIMES_PATH = os.path.join(DATA_PATH, "original/stop_times.txt")
TRIPS_PATH = os.path.join(DATA_PATH, "original/trips.txt")
ROUTES_PATH = os.path.join(DATA_PATH, "original/routes.txt")

SCHEDULE_DESTINATION_PATH = os.path.join(DATA_PATH, "schedules/schedule-" + str(int(time.time())) + ".csv")
SCHEDULE_FIELDNAMES = ["trip_id","departure_time","route_id", "trip_headsign", "route_short_name", "route_long_name"]

def write_csv_file(destination, fieldnames, rows):
	with open(destination, 'w') as file:
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(rows)

def sub_dict(somedict, somekeys, default=None):
	return dict([ (k, somedict.get(k, default)) for k in somekeys ])

def get_stop_times_for_stop_id(stop_id, stop_times_path=STOP_TIMES_PATH):
	with open(stop_times_path, 'rb') as csvfile:
		stop_times = csv.DictReader(csvfile, delimiter=',')
		return filter(lambda row: row['stop_id'] == stop_id, stop_times)

def append_trip_fields_to_schedule(schedule, trips_path=TRIPS_PATH):
	with open(trips_path) as trips_file:
		trips = csv.DictReader(trips_file)
		sorting_key = operator.itemgetter("trip_id")
		schedule = sorted(schedule, key=sorting_key)  # should already be the case
		trips = sorted(trips, key=sorting_key)

		# TODO can be improved by just using zip from the index of the first trip_id match (I think?)
		tripIndex = 0;
		for bus in schedule:
			tripEntry = next({"trip": trip, "index": index} for index, trip in enumerate(trips) if trip["trip_id"] == bus["trip_id"])
			tripIndex = tripEntry["index"]
			bus.update(tripEntry["trip"])
		return schedule


def append_route_fields_to_schedule(schedule, routes_path=ROUTES_PATH):
	with open(routes_path) as routes_file:
		routes = csv.DictReader(routes_file)
		sorting_key = operator.itemgetter("route_id")
		schedule = sorted(schedule, key=sorting_key)
		routes = sorted(routes, key=sorting_key)  # should already be the case
		
		# TODO can be improved by just using zip from the index of the first trip_id match (I think?)
		routeIndex = 0;
		for bus in schedule:
			routeEntry = next({"route": route, "index": index} for index, route in enumerate(routes) if route["route_id"] == bus["route_id"])
			routeIndex = routeEntry["index"]
			bus.update(routeEntry["route"])
		return schedule


def create_schedule(stop_id):
	schedule = get_stop_times_for_stop_id(stop_id)
	append_trip_fields_to_schedule(schedule)
	append_route_fields_to_schedule(schedule)
	schedule = map(lambda bus: sub_dict(bus, SCHEDULE_FIELDNAMES), schedule)

	# TODO sort by times/route_id??

	write_csv_file(SCHEDULE_DESTINATION_PATH, SCHEDULE_FIELDNAMES, schedule)

create_schedule(UPPSALA_POLACKSBACKEN_STOP_ID)




