# SRE Challenge: CI Build Metrics Collector

**Scenario Context**  
Your CI system provides a REST API endpoint that returns JSON data about recent builds, including build IDs, durations (in seconds), statuses, and timestamps. Engineering leadership wants a script to fetch the last 50 builds across multiple pipelines, compute average build time, count failed builds, and identify any builds exceeding the average by more than 50%.

---

## Task Requirements
1. **Fetch** build data from a paginated API endpoint:
   ```
   GET https://ci.example.com/api/v1/builds?page={n}&limit=10
   ```
2. **Handle** HTTP errors and retry failed requests up to 3 times.
3. **Parse** the JSON response, aggregating fields:
   - `build_id` (string)
   - `duration_seconds` (number)
   - `status` ("success", "failure", "unstable", etc.)
   - `timestamp` (ISO 8601 string)
4. **Compute**:
   - Total number of builds fetched
   - Average build duration
   - Number and percentage of failed builds
   - List of build IDs where `duration_seconds` > average × 1.5
5. **Output** a report in CSV format (`ci_build_report.csv`) with columns:
   ```
   build_id,duration_seconds,status,timestamp,above_threshold
   ```
   where `above_threshold` is `yes` or `no`.

---

## Input Format (sample API JSON)
```json
{
  "page": 1,
  "limit": 10,
  "total": 50,
  "builds": [
    {
      "build_id": "abc123",
      "duration_seconds": 240,
      "status": "success",
      "timestamp": "2025-07-30T08:15:22Z"
    },
    {
      "build_id": "def456",
      "duration_seconds": 450,
      "status": "failure",
      "timestamp": "2025-07-30T08:20:10Z"
    }
  ]
}
```

---

## Expected Output / Acceptance Criteria
- **Console summary**:
  ```
  Fetched 50 builds.
  Average duration: 300.00s.
  Failed builds: 5 (10.00%).
  Builds above threshold (450.00s): ["def456", "xyz789", ...]
  ```
- **CSV** `ci_build_report.csv` with all builds and an `above_threshold` flag.

---

## Suggested Extensions
- Add CLI flags for API URL, pagination size, and threshold multiplier.
- Cache results locally to avoid refetching unchanged pages.
- Produce a JSON summary in addition to CSV.
- Integrate email alerts when failure rate > 20%.

