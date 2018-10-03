import os.path
import csv
import time

UPPSALA_POLACKSBACKEN_STOP_ID = "740012548"

DATA_PATH = os.path.join("../data/")
STOP_TIMES_PATH = os.path.join(DATA_PATH, "original/stop_times.txt")
TRIPS_PATH = os.path.join(DATA_PATH, "original/trips.txt")

SCHEDULE_DESTINATION_PATH = os.path.join(DATA_PATH, "schedules/schedule-" + str(time.time()) + ".txt")
SCHEDULE_FIELDNAMES = ["trip_id","arrival_time","departure_time","stop_id","stop_sequence","pickup_type","drop_off_type", "route_id", "trip_headsign"]

def write_csv_file(destination, fieldnames, rows):
	with open(destination, 'w') as file:
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(rows)

def sub_dict(somedict, somekeys, default=None):
	return dict([ (k, somedict.get(k, default)) for k in somekeys ])

def get_stop_times_for_stop_id(stop_id):
	print('get_stop_times_for_stop_id=' + UPPSALA_POLACKSBACKEN_STOP_ID)
	with open(STOP_TIMES_PATH, 'rb') as csvfile:
		stop_times = csv.DictReader(csvfile, delimiter=',')
		return filter(lambda row: row['stop_id'] == stop_id, stop_times)

def append_trip_fields_to_schedule(schedule, trips_path):
	with open(trips_path) as trips_file:
		trips = csv.DictReader(trips_file)

		for bus in schedule:
			trip = next(trip for trip in trips if trip["trip_id"] == bus["trip_id"])
			bus.update(sub_dict(trip, ["route_id", "trip_headsign"]))

def create_schedule(stop_id):
	schedule = get_stop_times_for_stop_id(stop_id)
	append_trip_fields_to_schedule(schedule, TRIPS_PATH)
	write_csv_file(SCHEDULE_DESTINATION_PATH, SCHEDULE_FIELDNAMES, schedule)

create_schedule(UPPSALA_POLACKSBACKEN_STOP_ID)




