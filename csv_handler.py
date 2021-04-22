import csv
from next_date import next_generation_date
from datetime import datetime


def print_row(row):
    print(f' sys_ID: {row["systemid"]}, '
          f'profile: {row["profileid"]}, '
          f'frequency: {row["frequency"]}, '
          f'last_occ: {row["last_occurrence_date"]}'
          f'next_occ: {date_from_row(row)}'
          )


def date_from_row(row):
    # converts values from Row into datetime.date and grabs next_generation_date
    frequency = row["frequency"]
    create_date = row["create_date"]
    create_date = datetime.strptime(create_date, '%Y-%m-%d').date()
    print ('create date ok')
    last_occurrence_date = row["last_occurrence_date"]
    last_occurrence_date = datetime.strptime(last_occurrence_date, '%Y-%m-%d').date()
    print('last_occurance_ok')
    meta = [create_date, last_occurrence_date, frequency]
    return next_generation_date(*meta)


with open('next_rp.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:

        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            #line_count += 1
        #print(f'\t{row["name"]} works in the {row["department"]} department, and was born in {row["birthday month"]}.')
        elif line_count == 20:
            print("Done!")
            break
        print_row(row)
        line_count += 1
        print('Number of rows, ', line_count)

    print(f'Processed {line_count} lines.')