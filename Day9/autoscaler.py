import csv
import json
from collections import defaultdict
from io import StringIO
from datetime import datetime,timedelta

def autoscaler():
    stats = defaultdict(lambda :[0,0])
    with open('./autoscale.log', 'r') as file:
        for line in file:
            line = line.strip()
            try:
               if line.startswith('{'):
                   jsonline = json.loads(line)
                   ts = jsonline['timestamp']
                   status = jsonline['status']
                   node = jsonline['node_count']
               else:
                   ts,event,nodec = line.split(',')
                   node = int(nodec)

               time = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
               ts_new = time.replace(minute=0, second=0, microsecond=0)

               stats[ts_new][0] += node
               stats[ts_new][1] += 1

            except(ValueError, json.JSONDecodeError) as e:
                print("Skipping bad line")
                continue

    for hour, (sum_nodes, cnt) in stats.items():
        avg = sum_nodes / cnt
    print(f"{avg:.1f}")
    print(cnt)

print(autoscaler())