import csv
import json
import re


def compliance():

    with open('./compliance.csv','r') as csvFile, \
            open('./policy.json','r') as jsonFile, \
            open('./scan.log','r') as logFile:
        #2025-07-25T02:03:15Z
        time = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')
        log = re.compile(r'ERROR|INFO|WARN|DEBUG|OUT|TRACE')
        hostId = re.compile(r'host\-[0-9]+')
        message = re.compile(r'\w+')

        sevcount = 0
        dictReader = csv.DictReader(csvFile, fieldnames = ['hostid','group','issuecode','severity'])
        host = {}
        issue = []
        code = []
        for idx, row in enumerate(dictReader):
            hid = row.get('hostid')
            issuecode = row.get('issuecode')
            issue.append(issuecode)
            unique = set(issue)



            if hid in host:
                sev = row.get('severity')
                c = row.get('issuecode')
                code.append(c)
                sevcount += 1
                host[hid] = {
                    "total_issues" : sevcount,
                "failed_policies": set(code),
                }

            else:

                severity = row.get('severity')
                c = row.get('issuecode')
                sevcount = 1
                host[hid] = {
                    "total_issues": sevcount,
                    "failed_policies": c,
                }

        c = 0
        for l in logFile:
            h = hostId.findall(l)
            if h[0] in host and "scan started" in l:
                p = time.findall(l)
                host[h[0]]["scan_started_timestamp"] = p
            if h[0] in host and "ERROR" in l:
                c += 1
                host[h[0]]["scan_errors"] = c

        for j in jsonFile:

        print(host)








print(compliance())