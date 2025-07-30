# SRE Challenge: 5xx Error Rate Calculator

**Scenario Context**  
Your web service generates access logs in the common log format. Recently, you’ve seen intermittent 5xx errors in production. Your team SLO allows up to 0.5% 5xx errors over any 10-minute window. You need to write a script that parses the logs, calculates the 5xx error rate for each 10-minute interval, and flags intervals where the SLO is violated.

---

## Task Requirements
1. Parse a log file (`access.log`) in Common Log Format.  
2. Extract the timestamp and HTTP status code from each line.  
3. Group entries into 10-minute windows (e.g., 14:00–14:09, 14:10–14:19).  
4. Compute:
   - Total requests per window  
   - Number of 5xx errors per window  
   - 5xx error rate (errors / total)  
5. Output a report listing all windows where error rate > 0.5%, including:
   - Window start time  
   - Total requests  
   - Error count  
   - Error rate (percentage with two decimals)  

---

## Input Format (sample lines)
```
127.0.0.1 - - [2025-07-28:14:01:22 -0500] "GET /api/users HTTP/1.1" 200 512
127.0.0.1 - - [2025-07-28:14:03:45 -0500] "POST /api/orders HTTP/1.1" 500 1024
127.0.0.1 - - [2025-07-28:14:07:10 -0500] "GET /health HTTP/1.1" 503 64
...  
```

---

## Expected Output / Acceptance Criteria
- The script prints or writes a CSV report `error_report.csv` with columns:
  ```
  window_start,total_requests,error_count,error_rate_percent
  ```
- Only windows where `error_rate_percent > 0.50` are included.
- The error rate is rounded to two decimal places.

**Example output**:
```
2025-07-28T14:00:00-05:00,150,2,1.33
2025-07-28T14:10:00-05:00,180,3,1.67
```

---

## Suggested Extensions
- Accept a CLI flag to set window length (e.g., `--window=5` for 5 minutes).
- Generate a time series plot of error rate over the last 24 hours.
- Support parsing JSON-formatted logs.
- Send an alert (e.g., email) when a violation is detected in real time.
