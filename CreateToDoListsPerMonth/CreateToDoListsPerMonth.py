from datetime import date
from datetime import timedelta
import os

current_date = date.fromisoformat('2026-09-01') ## Change this
time_gap = timedelta(days = 1)
days_of_month = 30 ## Change this

directory_name = "C:\\Users\\Nicholli\\Documents\\InitialVault\\4. Daily Tasks\\September 2026" ## change this

## create directory if it doesn't already exist
if not(os.path.exists(directory_name)):
    os.makedirs(directory_name)

for i in range(0, days_of_month):
    file_contents = """
- [ ] breakfast
- [ ] take meds morning
- [ ] tech exercise
- [ ] exercise
- [ ] take meds night

***

Previous Day: [[{prev_day}]]
Next Day: [[{next_day}]]

""".format(current_day = current_date,
           prev_day = current_date - time_gap, 
           next_day = current_date + time_gap)

    ## prepend text
    prepend_text = ""

    ## add prepend only on weekdays
    day_of_week = current_date.isoweekday()
    if(day_of_week < 5):
        prepend_text = "- [ ] pick up Abigail" + prepend_text

    prepend_text = "## {current_day_text}\r\n".format(current_day_text = current_date.strftime("%A")) + prepend_text
    file_contents = prepend_text + file_contents

    ## write text to file
    with open (directory_name + "\\{current_day}.md".format(current_day = current_date), "w") as file_stream:
        file_stream.write(file_contents)
        print("Succesfully printed {current_day}".format(current_day = current_date))

    ## iterate to next day
    current_date = current_date + time_gap