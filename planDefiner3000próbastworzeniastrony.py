# planDefiner3000.py
import os
from tabulate import tabulate
from decoder import decode_subj_file
from planFinder import define_all_plans
from webWriter import get_hours

table = lambda df: tabulate(df, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], tablefmt='presto')

def main(file_to_read):
    file_to_write = "Schedules_" + os.path.basename(file_to_read)
    get_hours(file_to_read)
    schedules = open(os.path.join(os.path.dirname(file_to_read), file_to_write), "w+", encoding="utf-8")
    
    excluded_subjects = []
    start_hour = 1

    subjects, groups = decode_subj_file(file_to_read, os.path.dirname(file_to_read))
    executable_schedules = define_all_plans(subjects, groups, start_hour, excluded_subjects)

    possibilities = 1
    for k in range(len(subjects)):
        if subjects[k] not in excluded_subjects:
            possibilities *= len(groups[k])

    print('Found '+ str(len(executable_schedules)) + ' out of '+str(possibilities) + ' Sets.')

    for i in range(len(executable_schedules)):
        schedules.write(str(i+1)+'.\n')
        schedules.write(table(executable_schedules[i]))
        schedules.write("\n\n\n")
    schedules.close()

if __name__ == "__main__":
    file_path = input("Enter file name with hours: ")
    main(file_path)
