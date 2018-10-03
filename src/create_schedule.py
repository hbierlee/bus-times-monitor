import os.path
import csv
import time
print(time.time())
print(type(time.time()))

UPPSALA_POLACKSBACKEN_STOP_ID = "740012548"

DATA_PATH = os.path.join("../data/")
STOP_TIMES_PATH = os.path.join(DATA_PATH, "original/stop_times_small.txt")
SCHEDULE_DESTINATION_PATH = os.path.join(DATA_PATH, "schedules/schedule-" + str(time.time()) + ".txt")

def write_csv_file(destination, fieldnames, rows):
	print('start writing ')
	with open(destination, 'w') as file:
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(rows)

def find_all_stop_times_for_stop_id(stop_id):
	with open(STOP_TIMES_PATH, 'rb') as csvfile:
		stop_times = csv.DictReader(csvfile, delimiter=',')
		print('filtering stop_times on stop_id=' + UPPSALA_POLACKSBACKEN_STOP_ID)
		
		filtered_stop_times = filter(lambda row: row['stop_id'] == stop_id, stop_times)

		print(filtered_stop_times)

		write_csv_file(SCHEDULE_DESTINATION_PATH, stop_times.fieldnames, filtered_stop_times)


find_all_stop_times_for_stop_id(UPPSALA_POLACKSBACKEN_STOP_ID)




