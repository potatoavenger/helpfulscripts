import calendar as cal
import datetime as dt
from datetime import date, timedelta 
import os 
import argparse

# Constants
TIME_GAP = timedelta(days = 1)
BREAKFAST = "- [ ] breakfast\n"
MEDS_MORNING = "- [ ] take meds morning\n"
MEDS_NIGHT = "- [ ] take meds night\n"
TECH_EXERCISE = "- [ ] tech exercise\n"
EXERCISE = "- [ ] exercise\n"
PICK_UP = "- [ ] pick up gf\n" 
TRASH = "- [ ] trash bin\n" 
MAIL = "- [ ] mail\n" 
BUDGET = "- [ ] budget\n" 
TODO_LIST = "- [ ] to do list\n"
BACKUP_OBSIDIAN = "- [ ] backup Obsidian\n"


def determine_days_in_month(month):
    ## do not care about leap years
    match month:
        case cal.JANUARY | cal.MARCH | cal.MAY | cal.JULY | cal.AUGUST | cal.OCTOBER | cal.DECEMBER:
            return 31
        case cal.APRIL| cal.JUNE | cal.SEPTEMBER | cal.NOVEMBER:
            return 30
        case cal.FEBRUARY:
            return 28

def generate_special_todo_tasks(day):
    tasks = [BREAKFAST,MEDS_MORNING,MEDS_NIGHT,TECH_EXERCISE,EXERCISE]

    day_of_week = day.isoweekday()

    if day_of_week < 5: # only on weekdays minus Friday
        tasks.append(PICK_UP)

    if day_of_week == 2: # exery Tuesday
        tasks.append(TRASH)

    if day_of_week == 7:
        tasks.append(BACKUP_OBSIDIAN)

    if day_of_week == 1 or day_of_week == 4: # every Monday and Thursday
        tasks.append(MAIL)

    next_day = day + TIME_GAP 
    if next_day.month != day.month: # last day of the month
        tasks.append(BUDGET)
        tasks.append(TODO_LIST)
    

    return tasks


def generate_base_todo_list(day):
    default_list = generate_special_todo_tasks(day)

    footnote_navigation = """
***

Previous Day: [[{prev_day}]]
Next Day: [[{next_day}]]
""".format(prev_day = day - TIME_GAP, next_day = day + TIME_GAP)

    date_title = "## {current_day_text}\r\n".format(current_day_text = day.strftime("%A"))
    todo_tasks = date_title + "".join(default_list)
    return todo_tasks + footnote_navigation


def create_dir(day):
    base_dir = "C:\\Users\\Nicholli\\Documents\\InitialVault\\4. Daily Tasks"
    year_dir = base_dir + "\\{current_year}".format(current_year = day.year)
    if not(os.path.exists(year_dir)):
        os.makedirs(year_dir)

    month_dir = year_dir + "\\{current_month}".format(current_month = day.strftime("%B"))
    if not(os.path.exists(month_dir)):
        os.makedirs(month_dir)

    return month_dir


def write_to_file(directory_name, day, tasks):
    with open (directory_name + "\\{current_day}.md".format(current_day = day), "w") as file_stream:
        file_stream.write(tasks)
        print("Succesfully printed {current_day}".format(current_day = day))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("isodate", help="First date to be added in ISO format")
    args = parser.parse_args()

    current_day = dt.date.fromisoformat(args.isodate)
    tasks_dir = create_dir(current_day)
    number_days_in_month = determine_days_in_month(current_day.month)

    for i in range(0, number_days_in_month):
        tasks = generate_base_todo_list(current_day)
        write_to_file(tasks_dir, current_day, tasks)
        current_day = current_day + TIME_GAP

    
     
main()

