def get_some_time_ranges(start=8, to=16):
    r = []
    for hour in range(start, to):
        for minute in range(0, 59):
            r.append(datetime.datetime.combine(
                datetime.date.today(), datetime.time(hour, minute)))
    return r
