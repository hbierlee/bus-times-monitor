import csv
import itertools
import operator
import datetime

from schedule import CALENDAR_DATES_PATH, read_schedule


def get_services_for_schedule(schedule, path=CALENDAR_DATES_PATH):
    service_ids = set([bus["service_id"] for bus in schedule])

    with open(path) as file:
        services = csv.DictReader(file, delimiter=",")
        services = filter(
            lambda row: row["service_id"] in service_ids, services)
        services = sorted(services, key=operator.itemgetter(
            "service_id"))  # should already be the case
        services = itertools.groupby(
            services, key=operator.itemgetter("service_id"))

        # let value of service be just a sorted list of all service dates
        services = {key: sorted([service["date"] for service in value])
                    for key, value in services}
        return services


def is_service_available_for_date(service_id, services, date=datetime.date.today()):
    return service_id in services and date.strftime("%Y%m%d") in services[service_id]


# TODO possibly could also omit calendar_dates that are in the past
# TODO use bisect to search efficiently through sorted list in is_service_available_for_date
