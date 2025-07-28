## 1. Scenario

You operate a payments microservice behind an API gateway. During peak traffic the on‑call dashboard shows increased latency and intermittent 5xx errors. You have only the raw nginx access log from one pod (rotated daily) to quickly estimate whether you are burning the monthly error budget too fast.

- **SLO:** 99.9% success (≤0.1% errors allowed)  
- **Month length assumption:** 30 days → total minutes = 43,200  
- **Allowed error requests:** 0.1% of total requests (approximate from sampled log)  
- **Objective:** Approximate current burn rate over the last rolling 60 minutes.

## 2. Task

Write a Python script `analyze_errors.py` that:

1. **Reads** a gzip-compressed access log file `access.log.gz` as a stream.  
2. **Parses** each line with a regex extracting:  
   - `timestamp` (UTC)  
   - `status` (HTTP status code)  
   - `path` (URI path)  
   - `latency_ms` (custom field at end)  
3. **Filters** to lines within the last 60 minutes relative to the **max timestamp** observed in the file.  
4. **Counts:**  
   - `total_requests`  
   - `error_requests` (status ≥ 500)  
   - **Top 3 endpoints** by path prefix (first two segments, e.g. `/api/payments`) contributing to errors  
   - **95th percentile latency** (p95) across all requests in the window  
5. **Computes:**  
   - `error_rate_pct` for the 60‑min window  
   - **Projected monthly burn** = (current_hour_error_rate / allowed_error_rate_per_hour), where `allowed_error_rate_per_hour = 0.1%`  
   - **Flag** if `projected_monthly_burn_multiple > 24` (burn budget in <1 day)  
6. **Handles exceptions:**  
   - Skip & count malformed lines, time parsing failures, gzip read errors  
   - On fatal errors, print JSON `{"error":"<message>"}` and exit non-zero  
7. **Outputs** a single-line JSON to stdout:
   ```json
   {
     "window_start": "...",
     "window_end":   "...",
     "total_requests": 0,
     "error_requests": 0,
     "error_rate_pct": 0.0,
     "p95_latency_ms": 0,
     "top_error_endpoints": [
       {"path_prefix": "/api/payments", "errors": 0, "error_rate_pct": 0.0}
     ],
     "projected_monthly_burn_multiple": 0.0,
     "budget_burn_alert": false
   }
   ```

## 3. Sample Log Lines (nginx custom format)

```
2025-07-19T11:59:45Z "GET /api/payments/charge?id=123" 200 123ms
2025-07-19T12:00:12Z "POST /api/payments/refund" 502 987ms
2025-07-19T12:15:07Z "GET /api/users/profile" 200 45ms
2025-07-19T12:33:21Z "GET /api/payments/charge?id=999" 504 650ms
2025-07-19T12:40:05Z "GET /api/payments/history" 200 420ms
2025-07-19T12:55:55Z "POST /api/payments/refund" 500 1100ms
```
*(Actual file is gzip-compressed.)*

## 4. Acceptance Criteria

- Works when piping: `zcat access.log.gz | python analyze_errors.py` (optional) or reads gzip directly  
- Produces valid single-line JSON even on error  
- Single-pass processing (you may store last timestamp while iterating)  
- Regex robust to query strings and complex paths  
- p95 computed correctly (use minimal in-memory list for latencies within the window)  
- Percentages rounded to 3 decimal places

## 5. Suggested Extensions (Optional)

- Add latency buckets histogram  
- Support configurable rolling window (`--window-mins`)  
- Add threshold-based exit codes (e.g., exit 2 if alert)  
- Stream output as NDJSON for multiple windows  
