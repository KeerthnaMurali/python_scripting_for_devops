## 1. Scenario

Your SRE team runs a nightly “drift detection” job that compares the current state of deployed services to a known “golden” configuration. Each run produces:

- A CSV of service versions actually running
- A JSON file of the expected versions
- A plain‑text log of validation events

You need a utility that ingests all three artifacts, detects any version mismatches, computes statistics (e.g. mismatch rates), and schedules a follow‑up report if the mismatch rate exceeds a threshold.

## 2. Task Requirements

Write a Python script `config_drift_report.py` that:

1. **Reads:**
   - `running.csv` (columns: `service,region,version`)
   - `expected.json` (structure: `{"services":[{"name":"svc-A","version":"1.2.3"},…]}`)
   - `drift.log` (plain‑text lines like `2025-07-23T01:15:22Z INFO svc-A version drift detected: running=1.2.2 expected=1.2.3`)

2. **Parses:**
   - CSV via the `csv` module (streamed, no full load)
   - JSON via `json`
   - Log via a regex to extract `timestamp`, `level`, `service`, `running_version`, and `expected_version`

3. **Handles exceptions:**
   - Missing files → exit with JSON `{"error":"<message>"}` and non-zero code
   - Malformed CSV row, bad JSON, or log lines that don’t match regex → skip & count them

4. **Builds** a dictionary mapping each service to:
   ```python
   {
     "svc-A": {
       "running_version":    "1.2.2",
       "expected_version":   "1.2.3",
       "drift_detected":     True,
       "first_drift_time":   "2025-07-23T01:15:22Z"  # or null
     },
     …
   }
   ```

5. **Calculates:**
   - `total_services`
   - `drift_count` (number of services where `drift_detected` is True)
   - `drift_rate_pct = (drift_count / total_services) * 100`

6. **Schedules a follow‑up action if** `drift_rate_pct > 5%`:
   ```yaml
   Scheduling follow-up: drift rate 7.5% exceeds 5% threshold.
   Next check at 2025-07-24T01:00:00Z
   ```
   Compute “next check” as 24 hours after the latest log timestamp.

7. **Outputs** a single‑line JSON summary to stdout:
   ```json
   {
     "generated_at":"2025-07-23T02:00:00Z",
     "total_services": 50,
     "drift_count": 4,
     "drift_rate_pct": 8.0,
     "services": {
       "svc-A":{"running":"1.2.2","expected":"1.2.3","drift_detected":true,"first_drift_time":"2025-07-23T01:15:22Z"},
       "svc-B":{"running":"2.0.0","expected":"2.0.0","drift_detected":false,"first_drift_time":null},
       …
     },
     "malformed_csv": 1,
     "malformed_json": 0,
     "malformed_log": 2
   }
   ```

## 3. Input Format

**running.csv**
```csv
svc-A,us-east-1,1.2.2
svc-B,us-west-2,2.0.0
...
```

**expected.json**
```json
{"services":[{"name":"svc-A","version":"1.2.3"},{"name":"svc-B","version":"2.0.0"},…]}
```

**drift.log**
```text
2025-07-23T01:15:22Z INFO svc-A version drift detected: running=1.2.2 expected=1.2.3
2025-07-23T01:20:10Z WARN svc-C version drift detected: running=3.1.0 expected=3.1.1
…
```

## 4. Acceptance Criteria

- Streams CSV; never loads entire file  
- Gracefully skips & counts any malformed rows, JSON, or log lines  
- Correctly matches services across CSV and JSON  
- Accurately computes drift statistics  
- Calculates “next check” as 24 h after the latest log timestamp  
- Prints scheduling message only if drift rate > 5%  
- Emits exactly one valid JSON summary (or an error JSON on fatal failure)

## 5. Suggested Extensions

- Add CLI flags for threshold and schedule interval (e.g., `--threshold 3` or `--interval-hours 12`)  
- Support compressed inputs (`.csv.gz`, `.json.gz`, `.log.gz`)  
- Export the services table as CSV for downstream tooling  
- Integrate with a calendar API (e.g., Google Calendar) to create the follow-up event automatically
