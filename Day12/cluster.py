import json
import re
import csv
from collections import defaultdict


def cluster_script():

    with open('./input.json','r') as jsonFile:
        failed_pods = 0
        running_pods = 0
        pods = 0
        seen =set()
        stats = defaultdict(lambda: [0, 0])
        data = json.load(jsonFile)

        for d in data:
            cluster = d['cluster']
            namespace= d['namespace']
            app =d['app']
            key = (cluster,namespace,app)
            if d['status'] != "Running":
                stats[key][1] +=1
            else:
                stats[key][0]+=1


    with open('./pod_health_report.csv','a') as csvFile:
        writer = csv.DictWriter(csvFile,fieldnames=['cluster', 'namespace','app', 'running_pods', 'failed_pods','total_pods'])
        writer.writeheader()
        for (cluster, namespace, app), (running_pods, failed_pods) in stats.items():
            writer.writerow({'cluster':cluster,'namespace':namespace, 'app': app, 'running_pods':running_pods,'failed_pods':failed_pods, 'total_pods':pods})


print(cluster_script())