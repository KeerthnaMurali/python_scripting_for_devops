import re
import json
from datetime import datetime, timedelta
import csv

def error_rate():
    status_code = re.compile(r'[1-5]{1}[0-5]{2}')
    error_code = re.compile(r'5|4[0-5]{2}')
    timestamp = re.compile(r'\d{4}-\d{2}-\d{2}:\d{2}:\d{2}:\d{2} -0500')
    total_req = 0
    err_count = 0

    with open('./access.log','r') as file, \
            open('./output12.csv', 'w', newline='') as csvFile:
        fieldnames = ['window_start', 'total_requests', 'error_count', 'window_end']
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        writer.writeheader()

        lines = file.readlines()
        for l in lines:
            err = status_code.findall(l)
            ts = timestamp.findall(l)
            if ts:
                window_start = datetime.strptime(ts[0], "%Y-%m-%d:%H:%M:%S %z")

        end = window_start +timedelta(minutes=10)
        for line in lines:
            code = status_code.findall(line)
            ts = timestamp.findall(line)
            e = error_code.findall(line)
            if not ts:
                continue
            current = datetime.strptime(ts[0], "%Y-%m-%d:%H:%M:%S %z")
            if window_start <= current < end:
                if code[0] in line:
                    total_req += 1

                if e[0] in line:
                    err_count += 1

             # Writes column headers
        writer.writerow({'window_start': window_start, 'total_requests': total_req, 'error_count': err_count,'window_end': end})











print(error_rate())