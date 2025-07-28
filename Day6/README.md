## 1. Scenario

Your monitoring stack collects periodic host health snapshots in a central log file. Each line is a JSON object describing CPU, memory, and disk usage at a timestamp. Late-night maintenance jobs inject partial or malformed JSON entries, so you need a robust utility to:

- Ingest the JSON‑lines log  
- Discard bad entries but report how many were skipped  
- Filter entries to a specific time window  
- Aggregate per‑host health metrics  
- Emit a consolidated JSON summary for dashboards  

## 2. Task Requirements

Write a Python script `health_summary.py` that:

1. **Reads** a file `host-health.jsonl` line by line (don’t load the whole file).

2. **Parses** each line as JSON and validates it contains:  
   - `"host_id"` (string)  
   - `"timestamp"` (ISO 8601 UTC, e.g. `"2025-07-23T02:15:00Z"`)  
   - `"metrics"` (dict with keys `"cpu_pct"`, `"mem_pct"`, `"disk_pct"`)

3. **Handles exceptions:**  
   - Skips and counts any lines that are not valid JSON or are missing required fields.

4. **Filters** entries whose `"timestamp"` falls between `--start` and `--end` CLI arguments (both ISO 8601). If omitted, defaults to the last 6 hours from now.

5. **Aggregates** for each `host_id` over that window:  
   - **Average CPU utilization** (`cpu_pct`)  
   - **Peak memory utilization** (`mem_pct`)  
   - **Maximum disk utilization** (`disk_pct`)

6. **Outputs** a single‑line JSON summary to stdout:
   ```json
   {
     "window_start": "2025-07-23T00:00:00Z",
     "window_end":   "2025-07-23T12:00:00Z",
     "hosts": {
       "host-01": {
         "avg_cpu_pct":  42.3,
         "peak_mem_pct": 78.9,
         "max_disk_pct": 62.1
       },
       "host-02": { … }
     },
     "malformed_lines": 5
   }
   ```

7. **CLI Arguments:** Accepts `--start` and `--end`; if omitted, defaults to the last 6 hours from now.

8. **Constraints:** Use only the Python standard library and memory-efficient streaming.

## 3. Input Format (sample `host-health.jsonl`)

```jsonl
{"host_id":"host-01","timestamp":"2025-07-23T02:00:00Z","metrics":{"cpu_pct":40.2,"mem_pct":65.5,"disk_pct":60.1}}
{"host_id":"host-02","timestamp":"2025-07-23T02:05:00Z","metrics":{"cpu_pct":55.0,"mem_pct":70.3,"disk_pct":58.2}}
MALFORMED JSON LINE
{"host_id":"host-01","timestamp":"2025-07-23T05:15:00Z","metrics":{"cpu_pct":44.5,"mem_pct":78.9,"disk_pct":62.1}}
```