You are given a CSV file named timesheet.csv, where each row represents an employee’s work hours for a day:

bash
Copy
Edit
employee_id,date,clock_in,clock_out
✅ Your Task
Read the file timesheet.csv.

Validate each row:

employee_id must be a 6-digit number.

date must be a valid YYYY-MM-DD date.

clock_in and clock_out must be valid HH:MM 24-hour times.

clock_out must be after clock_in.

Skip invalid rows, and for each invalid row:

Write the line number and reason into a log file called errors.log.

For valid rows, calculate hours worked (rounded to 2 decimal places).

Write all valid results into valid_timesheet.csv in this format:

bash
Copy
Edit
employee_id,date,hours_worked
📁 Sample Input File: timesheet.csv
csv
Copy
Edit
employee_id,date,clock_in,clock_out
123456,2025-07-17,09:00,17:30
789012,2025-07-17,08:30,16:00
23456X,2025-07-17,10:00,18:00
345678,2025-07-17,14:00,12:00
✅ Expected Output File: valid_timesheet.csv
csv
Copy
Edit
employee_id,date,hours_worked
123456,2025-07-17,8.5
789012,2025-07-17,7.5
🪵 Expected Log File: errors.log
yaml
Copy
Edit
Line 4: Invalid employee_id
Line 5: clock_out earlier than clock_in
Would you like me to generate the starter Python code template for this now?




