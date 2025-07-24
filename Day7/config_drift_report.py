import csv
import json
import re
from datetime import datetime

def report():
    with open ('./running.csv', 'r') as csv_file, \
        open ('./drift.log', 'r') as log_file, \
        open ('./expected.json','r') as jsonFile:
        result = {}
        count = 0
        reVersion = re.compile(r'\d+\.\d+\.\d+')
        dictreader = csv.DictReader(csv_file)
        svcName = re.compile(r'[a-zA-Z0-9]+-[A-Z]+')
        for idx, row in enumerate(dictreader):
            runningVersion = row.get("version")
            serviceName = row.get("service")
            result[serviceName] = {
                    "running": runningVersion,
                }
        for line in log_file:
            if "detected" in line:
                svc_name = svcName.findall(line)
                if svc_name:
                    value = result.get(svc_name[0])
                    value['drift_detected'] = True
                    result[svc_name[0]] = value

        for line in jsonFile:
            data = json.loads(line)
            service = data['services']
            # print(service)
            for i in service:
                expected = i.get("version")
                # print(expected)
                svc = i.get("name")
                if svc in result:
                    #get the service
                    s = result.get(svc)
                    s["expected"] = expected

                    result[svc] = s

        print(result)













print(report())