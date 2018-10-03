import os.path
import csv

UPPSALA_POLACKSBACKEN_STOP_ID = "740012548"

DATA_PATH = os.path.join("../data/")
STOP_TIMES_PATH = os.path.join(DATA_PATH, "original/stop_times_small.txt")

def find_all_stop_times_for_stop_id(stop_id):
	with open(STOP_TIMES_PATH, 'rb') as csvfile:
		stop_times = csv.DictReader(csvfile, delimiter=',')
		print('filtering stop_times on stop_id=' + UPPSALA_POLACKSBACKEN_STOP_ID)
		return filter(lambda row: row['stop_id'] == stop_id, stop_times)


uppsala_polacksbackend_stop_times = find_all_stop_times_for_stop_id(UPPSALA_POLACKSBACKEN_STOP_ID)

print(uppsala_polacksbackend_stop_times)

