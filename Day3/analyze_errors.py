import gzip
import json
import re
import numpy as np
from datetime import datetime, timedelta
def analyzeErrors():
    timestamp = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z')

    uriPath = re.compile(r'\/api\/[a-z]+/\w+')


    countReq = 0
    with gzip.open('./access.log.gz', 'rt') as file:

        for line in file:
            time = timestamp.findall(line)
            matchTime = None

            for t in time:
                dT = datetime.strptime(t,'%Y-%m-%dT%H:%M:%SZ')
                if matchTime is None or dT > matchTime:
                    matchTime = dT


        start = matchTime - timedelta(minutes=60)
        # print(start)

    with gzip.open('./access.log.gz', 'rt') as f:
        for l in f:
            time = timestamp.findall(l)
            for t in time:
                date = datetime.strptime(t, '%Y-%m-%dT%H:%M:%SZ')

                if start < date and date < matchTime:
                    print(l)


            # if time in line:
            #     print(line)


class BudgetExceededError(Exception):
    pass


def totalRequests():
    count = 0
    status = re.compile(r'5[0-9]{2}')
    uriPath = re.compile(r'\/api\/[a-z]+/\w+')
    countFail = 0
    result = []
    error_rate_pct = 0
    projected_monthly_burn_multiple = 0
    with gzip.open('./access.log.gz', 'rt') as f:

        for line in f:
            failReq = status.findall(line)
            count += 1
            if failReq:
                countFail += 1
                api = uriPath.findall(line)
                for match in api:
                    result.append(match)
        print(result[:3])

        error_rate_pct = (countFail/count) * 100

        projected_monthly_burn_multiple = error_rate_pct / 0.1


        try:
            if projected_monthly_burn_multiple > 24:
                # include a message so you know why it failed
                raise BudgetExceededError(
                    f"Projected burn multiple {projected_monthly_burn_multiple:.2f} exceeds 24× threshold"
                )
            # …normal processing…
            print("Burn rate is within acceptable limits.")
        except BudgetExceededError as e:
            # handle your specific error
            print(f"🚨 ALERT: {e}")
            # you could re‑raise, log, send notification, etc.
        except Exception as e:
            # catch any other unexpected errors
            print(f"Unexpected error: {e}")
        else:
            # runs if no exception was thrown
            print("All good!")
        finally:
            # always runs
            print("Finished burn‑rate check.")
    return error_rate_pct, count, countFail, projected_monthly_burn_multiple

def percentile():
    latency = re.compile(r'\b\d+(?=ms\b)')
    result = []
    with gzip.open('./access.log.gz', 'rt') as file:
        for line in file:
            lat = latency.findall(line)
            for l in lat:
                result.append(int(l))

        result.sort()

        p = np.percentile(result, 95)
    return round(p,2)

def output():
    error_rate_pct, count, countFail, projected_monthly_burn_multiple = totalRequests()
    p = percentile()
    jsonOutput = {
        "error_percent": round(error_rate_pct, 2),
        "total_requests": count,
        "failed_5xx": countFail,
        "percentile": p
    }
    return json.dumps(jsonOutput, indent=2)

# print(output())

# print(percentile())




print(analyzeErrors())
# print(totalRequests())


