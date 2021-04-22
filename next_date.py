import calendar
import re
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pytz as pytz

FRESHBOOKS_TIMEZONE = pytz.timezone("US/Eastern")

# group = magnitude, \d any char not DEC, ? = 0 or 1 reps of the prev. expr. , group(unit) [anychar of 'ymw']
FREQUENCY_REGEX = re.compile(r"(?P<magnitude>\d+)?(?P<unit>[ymw])")
DURATION_UNIT_MAP = {"w": "weeks", "m": "months", "y": "years"}


def convert_to_datetime():
    return


def next_generation_date(create_date, last_occurrence_date, frequency):
    today = datetime.now(tz=FRESHBOOKS_TIMEZONE).date()
    if today < create_date:
        return create_date
    if not last_occurrence_date or last_occurrence_date < create_date:
        return create_date
    delta = time_delta_from_frequency(frequency)
    date_base = last_occurrence_date if last_occurrence_date else create_date
    if not delta:
        return None
    next_issue_date = date_base + delta
    next_issue_date = preserve_create_day_for_monthly_schedules(create_date, frequency, next_issue_date)
    return next_issue_date


def preserve_create_day_for_monthly_schedules(create_date, frequency, next_issue_date):
    if "m" not in frequency or create_date.day < 29:
        return next_issue_date
    last_day_of_month = calendar.monthrange(next_issue_date.year, next_issue_date.month)[1]
    next_issue_day = min(create_date.day, last_day_of_month)
    return date(next_issue_date.year, next_issue_date.month, next_issue_day)


def time_delta_from_frequency(frequency):
    match = FREQUENCY_REGEX.match(frequency)
    if match is None:
        return None
    magnitude = int(match.group("magnitude") or 1)
    duration_unit_string = DURATION_UNIT_MAP[match.group("unit")]
    return relativedelta(**{duration_unit_string: magnitude})







# choices = [1, 2, 3]
#
# while True:
#     choice = input('Which set of variables would you like to use? 1, 2, 3? ')
#     try:
#         choice = int(choice)
#         if choice in choices:
#             print('You chose ', choice)
#             break
#
#     except:
#         print('Bad drive!')

# if choice == 1:
#     create_date = date(2021, 1, 1)
#     last_occurrence_date = date(2022, 1, 1)
#     frequency = "3m"
# elif choice == 2:
#     create_date = date(2021, 3, 20)
#     last_occurrence_date = date(2021, 3, 20)
#     frequency = "1y"
# elif choice == 3:
#     create_date = date(2021, 1, 1)
#     last_occurrence_date = date(2023, 6, 15)
#     frequency = "5m"
#
# meta_date = (create_date, last_occurrence_date, frequency)
# for i in meta_date:
#     print(i)

# calculated_date = next_generation_date(*meta_date)
# print('    Calculated Next Date ===  ', calculated_date)

# def calc_next(create_date, last_occurrence_date, frequency):
#     calculated_date = next_generation_date(*meta_date)
#     print('calculating date: ', calculated_date)

''' 
-- original code to run program---
calculated_date = next_generation_date(create_date=date(2021, 1, 1),
                                       last_occurrence_date=date(2022, 1, 1),
                                       frequency="3m")
print(calculated_date)

"that is your howemork # 3, make this runnable and figure out how to use it to predict ‘next invoice date’ "

'''
