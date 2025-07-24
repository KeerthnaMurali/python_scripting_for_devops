import csv
import re
import json
from datetime import datetime, timedelta
def backup():
    pattern = re.compile(r'%Y-%m-%dT%H:%M:%SZ')
    end = timedelta(hours=24)
    due = datetime.now() + end
    now = datetime.now()
    regCount = 0
    with open('./backups.csv', mode='r',newline='') as f:
        reader = csv.DictReader(f)


        for idx, row in enumerate(reader, start=2):
            schedule = row.get("schedule_time", "").strip()
            jobid = row.get("job_id", "").strip()
            region = row.get("region", "").strip()
            time = datetime.strptime(schedule,"%Y-%m-%dT%H:%M:%SZ")
            if now <= time <= due:
                return region, time, jobid

















print(backup())