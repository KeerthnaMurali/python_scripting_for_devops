import csv
import re
from collections import defaultdict
from datetime import datetime,timedelta
import json
def alert():
    with open('./access.log', 'r') as logFile, \
        open('./certs.csv', 'r') as csvFile:

        ts = re.compile(r'\[(?P<ts>\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2}\s\+\d{4})\]')
        status = re.compile(r'50[1-5]{1}')
        endpoint_re = re.compile(r'/api/[A-Za-z0-9_-]+|/health|/metrics')
        pattern = re.compile(
            r'^(?P<domain>[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*),(?P<expiry>\d{4}-\d{2}-\d{2})$'
        )

        read = csv.DictReader(csvFile, fieldnames=['domain', 'expiry'])

        stats = defaultdict(lambda : { "total": 0, "error": 0, "error_rate_pct": 0})
        certs = []
        k = {}
        req = 0
        count_error = 0
        malformed = 0


        for line in logFile:
            ep = endpoint_re.findall(line)
            ereq = status.findall(line)
            if len(ep) != 0:
                endpoint = ep[0]
                if endpoint:
                    stats[endpoint]["total"] += 1
                    if len(ereq) != 0:
                        stats[endpoint]["error"] += 1
            else:
                malformed += 1
                # print(f"MALFORMED: {malformed}")

            # loop through stats dic to key value
        for key, value in stats.items():
            total = value.get("total")
            count = value.get("error")
            error_rate_pct = (count / total) * 100
            stats[key]["error_rate_pct"] = error_rate_pct

        for idx, row in enumerate(read):
            exp_date = datetime.strptime(row["expiry"],"%Y-%m-%d")
            now = datetime.now()
            now_date = now.date()

            edt = exp_date.date() - now_date

            days = timedelta(days=30)

            if edt < days:

                domain = row["domain"]

                k = {
                    "domain" : domain,
                    "days_until_expiry": str(edt)

                }
                certs.append(k)

        # print(certs)
        result = {
            "generated_at": str(datetime.now()),
            "errors": stats,
            "certs_expiring_soon": certs,
            "malformed_log_lines": malformed
        }

    return json.dumps(result,indent=4)


















        # for idx, row in enumerate(read):





print(alert())