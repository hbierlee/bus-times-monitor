import os.path
from schedule import create_schedule, write_csv_file, get_schedule_filename, SCHEDULES_FOLDER_PATH, SCHEDULE_FIELDNAMES


schedule = create_schedule()
write_csv_file(os.path.join(SCHEDULES_FOLDER_PATH, get_schedule_filename()), SCHEDULE_FIELDNAMES, schedule)
