import csv
from datetime import datetime
def timesheet():
    id = ""
    with open('timesheet.csv', mode='r', newline='') as f, \
         open('error_logfile', 'w') as err, \
            open('new_timesheet.csv', 'w', newline='') as out:
        csv_reader = csv.DictReader(f)
        csv_writer = csv.DictWriter(out, fieldnames=["employee_id", "date", "hours_worked"])
        csv_writer.writeheader()



        #now read every column:

        for idx, row in enumerate(csv_reader, start=2):
            emp_id = row.get("employee_id","").strip()
            date=row.get("date","").strip()
            clock_in=row.get("clock_in","").strip()
            clock_out = row.get("clock_out", "").strip()

            #Validate

            if not emp_id.isdigit() or len(emp_id)!=6:
                err.write(f"Line {idx}: Invalid employee_id\n")
                continue

            isValidDate = datetime.strptime(date,"%Y-%m-%d")

            if not isValidDate:
                err.write(f"Line {idx}: Invalid date")
                continue

            isValidclockin = datetime.strptime(clock_in,"%H:%M")
            isValidclockout = datetime.strptime(clock_out,"%H:%M")

            if not isValidclockin or not isValidclockout:
                err.write(f"Line {idx}: Invalid clockin or clock out \n")
                continue

            else:
                try:
                    hours = (isValidclockout - isValidclockin).seconds / 3600
                    total_hours = round(hours,2)
                    if total_hours <= 0:
                        raise ValueError("clock_out earlier than clock_in")

                    csv_writer.writerow({"employee_id": emp_id,
                "date": date,
                "hours_worked": hours})

                except Exception as e:
                    err.write(f"Line {idx}: {str(e)}\n")
                    continue



timesheet()









