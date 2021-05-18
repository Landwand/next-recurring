from process_profiles import *

profiles = read_profiles_from_file('next_rp2.csv')

for profile in profiles:
    convert_fields_to_datetime(profile)
    add_next_generation_date(profile)

file_name = 'final.csv'
write_profiles_to_csv(profiles, file_name)
print('Program completed')
