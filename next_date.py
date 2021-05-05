import calendar
import re
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pytz as pytz

FRESHBOOKS_TIMEZONE = pytz.timezone("US/Eastern")

# Winston's translation = group = magnitude, \d any char not DEC, ? = 0 or 1 reps of the prev. expr. , group(unit) [anychar of 'ymw']
FREQUENCY_REGEX = re.compile(r"(?P<magnitude>\d+)?(?P<unit>[ymw])")
DURATION_UNIT_MAP = {"w": "weeks", "m": "months", "y": "years"}


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
