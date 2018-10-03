import os.path
import csv
import time
import operator 

UPPSALA_POLACKSBACKEN_STOP_ID = "740012548"

DATA_PATH = os.path.join("../data/")
STOP_TIMES_PATH = os.path.join(DATA_PATH, "stop_times.txt")
TRIPS_PATH = os.path.join(DATA_PATH, "trips.txt")
ROUTES_PATH = os.path.join(DATA_PATH, "routes.txt")
CALENDAR_PATH = os.path.join(DATA_PATH, "calendar.txt")
CALENDAR_DATES_PATH = os.path.join(DATA_PATH, "calendar_dates.txt")

SCHEDULE_DESTINATION_PATH = os.path.join(DATA_PATH, "schedules/schedule-" + str(int(time.time())) + ".csv")
SCHEDULE_FIELDNAMES = ["trip_id", "route_id", "service_id", "route_short_name", "trip_headsign", "departure_time", "monday","tuesday","wednesday","thursday","friday","saturday","sunday","start_date", "end_date", "date", "exception_type"]

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


def inner_join_file_to_schedule(schedule, path, key):
	with open(path) as file:
		other_data = csv.DictReader(file)
		
		sorting_key = operator.itemgetter(key)
		schedule = sorted(schedule, key=sorting_key)
		other_data = sorted(other_data, key=sorting_key)
		
		# TODO can be improved by just using zip from the index of the first trip_id match (I think?)
		otherIndex = 0;
		for bus in schedule:
			routeEntry = next({"other": other, "index": index} for index, other in enumerate(other_data[otherIndex+1:]) if other[key] == bus[key])
			otherIndex = routeEntry["index"]
			bus.update(routeEntry["other"])
		return schedule


def create_schedule(stop_id):
	print("create_schedule")
	schedule = get_stop_times_for_stop_id(stop_id)
	inner_join_file_to_schedule(schedule, TRIPS_PATH, "trip_id")
	inner_join_file_to_schedule(schedule, ROUTES_PATH, "route_id")
	inner_join_file_to_schedule(schedule, CALENDAR_PATH, "service_id")
	inner_join_file_to_schedule(schedule, CALENDAR_DATES_PATH, "service_id")

	schedule = map(lambda bus: sub_dict(bus, SCHEDULE_FIELDNAMES), schedule)

	# TODO sort by times/route_id??

	write_csv_file(SCHEDULE_DESTINATION_PATH, SCHEDULE_FIELDNAMES, schedule)

create_schedule(UPPSALA_POLACKSBACKEN_STOP_ID)




