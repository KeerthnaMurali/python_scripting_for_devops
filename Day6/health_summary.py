import json
from itertools import count
from xml.etree.ElementTree import indent


def health():
    host = {}
    times = []
    malformed = 0
    with open('./health.jsonl', 'r') as file:


        for line in file:
            if not line:

                continue
            try:
                data = json.loads(line)

                id = data['host_id'] #get the id


                window_start = data['timestamp']

                times.append(data['timestamp'])

                if id in host:
                    hId = host.get(id)
                    # new_times = set(times)

                    # print(hId)

                    cpu = data['metrics']['cpu_pct']
                    peak_mem_pct = data['metrics']['mem_pct']
                    max_disk_pct = data['metrics']['disk_pct']

                    avg_cpu = (hId.get("avg_cpu_pct") + cpu) /2

                    avg_peak_mem_pct  = (hId.get("peak_mem_pct") + peak_mem_pct) /2

                    avg_max_disk_pct = (hId.get("max_disk_pct") + max_disk_pct) /2

                    hId = {
                            "avg_cpu_pct": avg_cpu,
                            "peak_mem_pct": avg_peak_mem_pct,
                            "max_disk_pct": avg_peak_mem_pct,
                        }

                    host[id] = hId
                else:

                    host[id] = {
                        "avg_cpu_pct" : data['metrics']['cpu_pct'],
                        "peak_mem_pct": data['metrics']['mem_pct'],
                        "max_disk_pct": data['metrics']['disk_pct'],
                    }


            except json.JSONDecodeError as e:
                malformed += 1
                print(f"Error parsing line {e}")

        # print(times)

        result = json.dumps({
            "window_start": times[1],
            "window_end": times[2],
            "hosts": host
        })

    return result





print(health())

