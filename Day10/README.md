## 1. Scenario

Your team collects daily NGINX access logs and periodically snapshots SSL certificate expirations into a CSV. You need a tool to:

- **Parse the access logs** to find 5xx error rates per endpoint  
- **Read the certificate CSV** to detect certificates expiring within 30 days  
- **Merge** these findings into a unified alert report  

---

## 2. Task Requirements

Write a Python script `alert_report.py` that:

1. **Reads two files**  
   - `access.log` (plain text, standard NGINX “combined” format)  
   - `certs.csv` (columns: `domain`, `expires_on` where `expires_on` is `YYYY-MM-DD`)  

2. **Parses**  
   - **Log lines** via regex to extract:  
     - `timestamp` (e.g. `10/Jul/2025:14:32:07 +0000`)  
     - `status` (HTTP code)  
     - `endpoint` (path portion of the URL)  
   - **CSV rows** via `csv.reader` for `domain` and `expires_on`  

3. **Handles exceptions**  
   - **Missing file** → print JSON `{"error": "…"} ` and exit nonzero  
   - **Malformed log line** or **bad date** → skip the entry & count it  

4. **Aggregates**  
   - **For the last 24 hours** (relative to the max log timestamp):  
     - Total requests and 5xx errors per endpoint  
     - Compute `error_rate_pct = errors / total × 100`  
   - **For certificates**:  
     - Parse each `expires_on` into a `date`  
     - Compute `days_until_expiration`  

5. **Builds a nested dictionary** with this structure:

    ```python
    report = {
        "endpoints": {
            "/api/foo": {
                "total_requests": 1234,
                "error_requests":  45,
                "error_rate_pct":  3.65
            },
            "/health": {
                "total_requests": 9876,
                "error_requests":   0,
                "error_rate_pct":   0.0
            },
            # … more endpoints …
        },
        "certs": {
            "example.com": {
                "expires_on":           "2025-08-15",
                "days_until_expiration": 18
            },
            "api.example.org": {
                "expires_on":           "2025-09-01",
                "days_until_expiration": 34
            },
            # … more domains …
        },
        "malformed": {
            "log_lines": 5,
            "csv_rows":  2
        }
    }
    ```

6. **Outputs** the `report` as pretty‑printed JSON to `stdout`.  

---  

**Optional Enhancements**  
- Add CLI flags for thresholds and time windows (e.g. `--threshold`, `--days`)  
- Support compressed inputs (`.log.gz`, `.csv.gz`)  
