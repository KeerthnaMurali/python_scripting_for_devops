import csv
import json
from collections import defaultdict

import requests
def metrics():
    global buildID, statusBuild, time
    total_builds = 0
    retries=3
    duration = 0
    failedBuild = 0
    b = ""
    s=""
    t=""
    du = 0
    status = {500,501,502,503,504}
    slow = []
    for attempt in range(1,retries+1):
        try:
            url = 'http://localhost:3000/builds'
            response = requests.get(url, timeout=5)
            if response.status_code in status:
                response.raise_for_status()
        except requests.RequestException as e:
            if attempt == retries:
                print(f"{attempt} attempts reached {e}")

    data = response.json()

    for d in data:
        total_builds += 1
        duration += d['duration_seconds']
        avg_duration = duration/total_builds
        statusBuild = d['status']
        if statusBuild != "success":
            failedBuild += 1
        time = d['timestamp']
        buildID = d['build_id']
        percent = (failedBuild/total_builds)*100
        above = avg_duration * 1.5
        if d['duration_seconds']>above:
            slow.append({'build_id':d['build_id'],
                         'duration_seconds': d['duration_seconds'],
                         'status': d['status'],
                         'timestamp': d['timestamp'],
                         'above_threshold': round(above, 2)})

        with open('./ci_build_report.csv', 'w') as csvFile:
            writer = csv.DictWriter(csvFile, fieldnames=['build_id', 'duration_seconds', 'status', 'timestamp',
                                                         'above_threshold'])
            writer.writeheader()
            for row in slow:
                writer.writerow(row)


print(metrics())
