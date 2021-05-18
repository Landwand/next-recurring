from dataclasses import dataclass
from dataclass_csv import DataclassReader, DataclassWriter
from datetime import datetime
from next_date import next_generation_date as calc_next_generation_date


# define dataclass to store each recurring template
@dataclass
class Profile:
    systemid: int
    profileid: int
    organization: str = None
    fname: str = None
    lname: str = None
    bill_name: str = None
    amount: float = None
    currency_code: str = None
    create_date: str = None
    frequency: str = None
    number_recurring: int = None
    discount_total: int = None
    discount_value: int = None
    due_offset_days: int = None
    description: str = None
    notes: str = None
    include_unbilled_time: str = None
    po_number: str = None
    card_saved: bool = False
    occurrences_to_date: int = None
    last_occurrence_date: str = None
    last_invoice_date: str = None
    next_generation_date: str = None


def read_profiles_from_file(file):
    profiles = []
    with open(file) as file:
        reader = DataclassReader(file, Profile)
        count = 0
        for profile in reader:
            profiles.append(profile)
            count += 1
        return profiles


def print_fields(profile):
    print(profile)
    print('systemid = ', profile.systemid)
    print('profileid = ', profile.profileid)
    print('create_date = ', profile.create_date)
    print('last_invoice_date = ', profile.last_invoice_date)
    print('next_occurrence_date = ', profile.next_occurrence_date)


def convert_fields_to_datetime(profile):
    fields = (
        'create_date',
        'last_invoice_date',
        'last_occurrence_date'
    )

    for field in fields:
        attribute = getattr(profile, field, )
        if attribute:
            date_obj = datetime.strptime(attribute, "%Y-%m-%d").date()
        else:
            date_obj = str('')
        setattr(profile, field, date_obj)


def str_to_datetime(field):
    if field:
        print(f' Converting, {field} to datetime format.')
        converted = datetime.strptime(field, "%Y-%m-%d")
        print('converted ', converted)
        print('type ', type(converted))
    else:
        converted = str('')
    return converted


def add_next_generation_date(profile):
    """    Inserts STR value, not datetime.date . """
    if profile.next_generation_date:
        return profile
    else:
        next_generation_date = calc_next_generation_date(
            create_date=profile.create_date,
            last_occurrence_date=profile.last_occurrence_date,
            frequency=profile.frequency
        )
        setattr(profile, 'next_generation_date', next_generation_date)


def write_profiles_to_csv(profiles, file_name):
    with open(file_name, 'w') as new_file:
        csv_writer = DataclassWriter(new_file, profiles, Profile)
        csv_writer.write()

