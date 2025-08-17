from collections import defaultdict
from datetime import datetime, timedelta
from itertools import count

import requests
import json
import csv
import re

def health():
    retries = 3
    count = 0
    error_count, critical_count = 0,0
    response_code = {'501','502','503','504'}
    stats = defaultdict(list)
    error = defaultdict(lambda :{'error':0,'critical':0})
    pods = defaultdict(lambda: {'running': 0, 'failed': 0})
    for attempt in range(retries+1):
        try:
            response = requests.get('http://localhost:3000/serviceConfigs', timeout=5)


            if response.status_code in response_code:
                response.raise_for_status()
                break

        except requests.RequestException as e:
            if attempt == retries:
                print(f"{attempt} attempts reached {e}")

    data = response.json()
    for d in data:
        config = d['config'].split("|")
        app = d['service']
        for i in config:
            if len(i) != 14:
                print("Invalid")

            index_str = i[:4]
            value = i[4:]
            if not (index_str.isdigit() and value.isalnum()):
                print(f"Invalid format for {app}: {i!r}")
                return

            idx = int(index_str)
            stats[app].append((idx, value))


            # sorted_pairs = sorted(stats[app], key=lambda t: t[0])
            # stats[app] = [val for _, val in sorted_pairs]



    #step 2:

    with open('./logs_api.json','r') as jsonFile:
        data = json.load(jsonFile)
        entry = data['entries']
        time = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')

        for e in entry:
            print(e)
            # t = datetime.strptime(ts,'%Y-%m-%d %H:%M:%S')
            # diff = timedelta(hours=1)
            # print(t)

            if "ERROR" in e:
                error_count += 1
            if "CRITICAL" in e:
                critical_count +=1

    with open('./pods.json','r') as logFile:
        p = json.load(logFile)
        for d in p:
            namespace = d['namespace']
            app = d['app']
            cluster = d['cluster']

            key = (namespace,app,cluster)
            if d['status'] == "Running":
                pods[key]['running'] += 1
            else:
                # count += 1
                pods[key]['failed'] += 1

            total_pods = pods[key]['running'] + pods[key]['failed']
            healthy_percent = (pods[key]['running'] / total_pods) * 100



    with open('./output.csv', 'w') as csvFile:
        writer = csv.DictWriter(csvFile,fieldnames=[ 'service','config_sequence','error_hour','total_errors','total_critical','cluster','namespace','app','total_pods','healthy_percent'])
        writer.writeheader()
        for s,c in stats.items():
            for error,critical in error.items():
                for (cluster, ns, app), pod_counts in pods.items():
                    writer.writerow({'service':s,'config_sequence': c, 'error_hour': error_count,'total_critical' : critical_count, 'cluster': cluster,'namespace':namespace,'app':app,'total_pods':total_pods,'healthy_percent': healthy_percent})

        # for e in error:
        #     writer.writerow({'error_hour': error[0],'total_critical' : error[1]})
        #
        # for k in pods:
        #     writer.writerow({'cluster': cluster,'namespace':namespace,'app':app,'total_pods':total,'healthy_percent': count})








print(health())