import json
from datetime import datetime
from xml.etree.ElementTree import indent


def metrics():
    now = datetime.now()
    with open('./analyze.log', 'r') as file:
        hosts = {}
        for line in file:
            try:
                data = json.loads(line)
                id = data['host_id']
                if hosts.get(id):
                    # get the existing host value
                    unique_host = hosts.get(id)

                    # update metrics
                    # get
                    metrics = unique_host.get("unique_metrics")
                    # update
                    metrics.append(data["metric_name"])

                    # update metrics count
                    count = unique_host.get("metrics_count") + 1

                    # update the actual host key hosts[id]
                    hosts[id] = {
                        "metrics_count" : count,
                        "unique_metrics": metrics,
                        "avg_cpu_usage": 53.6
                    }
                else:
                    hosts[id] = {
                        "metrics_count": 1,
                        "unique_metrics": [data['metric_name']],
                        "avg_cpu_usage": 53.6
                    }
            except json.JSONDecodeError as e:
                print(f"Error parsing line {e}")

        result = {
            "generated_at": datetime.strftime(now, "%Y-%m-%dT%H:%M:%SZ"),
            "hosts": hosts,
        }

        r = json.dumps(result,indent=3)
        print(r)






print(metrics())