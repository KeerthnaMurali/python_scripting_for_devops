## 1. Scenario

Your infrastructure team maintains a CSV schedule of automated backups across multiple regions. Every day you need to:

- Identify which backups are due in the next 24 hours  
- Group them by region  
- Calculate average and maximum backup window durations  
- Produce a JSON report for the on-call rotation  

Occasional malformed rows or missing timestamps can corrupt dashboards, so your script must be resilient.

## 2. Task Requirements

Write a Python script `backup_schedule_report.py` that:

1. **Reads** a CSV file `backups.csv` in the current directory (streamed, not fully loaded).

2. **Parses** each row with columns:
   ```csv
   job_id,region,schedule_time,duration_min,description
   ```
   - `schedule_time` is an ISO timestamp (e.g. `2025-07-21T03:30:00Z`)  
   - `duration_min` is an integer

3. **Filters** rows whose `schedule_time` falls within the next 24 hours from the script’s run time.

4. **Aggregates** per region:
   - **jobs**: list of upcoming `job_id`s  
   - **avg_duration_min**: average `duration_min`  
   - **max_duration_min**: maximum `duration_min`

5. **Handles exceptions:**
   - Skip & count rows with parse errors (malformed timestamp, non-integer duration)  
   - If `backups.csv` is missing or unreadable → emit JSON error & exit non-zero

6. **Outputs** to stdout a single-line JSON object:
   ```json
   {
     "generated_at":    "2025-07-21T12:00:00Z",
     "regions": {
       "us-east-1": {
         "jobs":             ["job-123","job-789"],
         "avg_duration_min": 45.5,
         "max_duration_min": 60
       },
       "eu-west-2": {
         "jobs":             ["job-456"],
         "avg_duration_min": 30.0,
         "max_duration_min": 30
       }
     },
     "malformed_rows": 2
   }
   ```

7. **Constraints:** Use only the Python standard library and memory-efficient streaming.

## 3. Input Format

```csv
job-123,us-east-1,2025-07-21T03:30:00Z,60,Daily snapshot
job-456,eu-west-2,2025-07-21T18:45:00Z,30,Config backup
job-789,us-east-1,2025-07-22T02:15:00Z,31,Log archive
```

## 4. Acceptance Criteria

- Running `python backup_schedule_report.py` produces valid JSON.  
- Only jobs within the next 24 hours are listed.  
- A correct count of malformed or skipped rows is reported.  
- A non-zero exit occurs if the file can’t be read.

## 5. Suggested Extensions

- Add CLI flags `--window-hours` or `--region-filter`.  
- Support `.csv.gz` input transparently.  
- Emit output as pretty-printed JSON or CSV.  
- Integrate with Slack/email API to deliver the report automatically.  
