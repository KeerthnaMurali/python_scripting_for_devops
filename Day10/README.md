1. Scenario
Your team collects daily NGINX access logs and periodically snapshots SSL certificate expirations into a CSV. You need a tool to:

Parse the access logs to find 5xx error rates per endpoint

Read the certificate CSV to detect certificates expiring within 30 days

Merge these findings into a unified alert report

2. Task Requirements
Write a Python script alert_report.py that:

Reads two files:

access.log (plain text, standard NGINX combined format)

certs.csv (columns: domain,expires_on where expires_on is YYYY-MM-DD)

Parses:

Log via regex to extract:

timestamp (e.g. 10/Jul/2025:14:32:07 +0000)

status (HTTP code)

endpoint (path portion of the URL)

CSV via csv.reader for domain and expiration date

Handles exceptions:

Missing file → print JSON {"error": "…"}  and exit nonzero

Malformed log line or bad date → skip & count

Aggregates:

For the last 24 hours (relative to the max log timestamp):

Total requests and 5xx errors per endpoint

Compute error_rate_pct = errors / total × 100

For certificates:

Parse each expires_on into a date

Compute days until expiration

Builds a nested dictionary: