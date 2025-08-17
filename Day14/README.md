# SRE Challenge: End-to-End System Health and Config Audit

**Scenario Context**  
Your organization operates a fleet of microservices. You need to implement an end‑to‑end script that:

1. Fetches latest service configurations from a REST API.  
2. Validates and orders barcode‑style config strings.  
3. Parses daily syslog entries via API to analyze error trends.  
4. Aggregates Kubernetes pod health JSON data for cross‑cluster monitoring.

This combines string validation, API interaction, JSON and CSV processing, file handling, regex, log parsing, metrics calculation, and date/time grouping.

---

## Task Requirements

1. **Configuration Fetch & Validate**  
   - **API**: `GET https://config.example.com/api/v1/services/configs` → returns JSON array of `{"service": str, "config": str}`.  
   - **Validate** each `config` string:  
     - Pairs are `"<index><value>"` of total length 14 characters (4‑digit index + 10-char alphanumeric value), separated by `|`.  
     - Indexes must start at `0001`, increment by 1, and none repeat or skip.  
   - **Order** configs by index and extract the 10‑char values.

2. **Log Fetch & Error Trend Analysis**  
   - **API**: `GET https://logs.example.com/api/v1/logs?date={today}&page={n}&limit=100` → JSON `{ "entries": [str, …] }`.  
   - **Retry** failed requests up to 3 times with exponential backoff.  
   - **Parse** each entry string using regex to extract timestamp (`YYYY-MM-DD HH:MM:SS`), log level, and message.  
   - **Filter** only `ERROR` and `CRITICAL`, group by hour, compute counts.

3. **Pod Health Aggregation**  
   - **Read** local file `pods.json` with array of pod objects (`cluster`, `namespace`, `app`, `status`).  
   - **Group** by `(cluster, namespace, app)`, count running vs failed, compute healthy percent.

4. **Report Generation**  
   - Write a CSV `system_audit_report.csv` with columns:
     ```
     service,config_sequence,error_hour,total_errors,total_critical,cluster,namespace,app,total_pods,healthy_percent
     ```
   - Each row should combine one service’s config sequence and error count for a given hour and one pod‑health group.

---

## Input Formats

1. **Configs API** (sample):
   ```json
   [
     { "service": "auth", "config": "0001abcd1234ef56|0002ghij7890kl12" },
     { "service": "payment", "config": "0001mnop3456qr78|0002stuv9012wx34|0003yzab5678cd90" }
   ]
   ```

2. **Logs API** (sample):
   ```json
   {
     "entries": [
       "2025-07-31 13:45:10 ERROR Disk usage exceeded 85%",
       "2025-07-31 13:50:05 CRITICAL Out of memory",
       "... more lines ..."
     ]
   }
   ```

3. **Pods JSON** (`pods.json` sample):
   ```json
   [
     { "cluster": "us-west1", "namespace": "prod", "app": "auth", "status": "Running" },
     { "cluster": "us-west1", "namespace": "prod", "app": "auth", "status": "CrashLoopBackOff" }
   ]
   ```

---

## Expected Outputs / Acceptance Criteria

- **Validation**: Invalid configs → immediate `["Invalid configuration for <service>"]` return.  
- **Console Summary**:  
  ```
  Service audit complete.
  Service: auth → Configs: ["abcd1234ef","ghij7890kl"]
  Hour 13:00 → Errors: 1, Critical: 1
  Cluster us-west1 prod auth → Pods: 2, Healthy: 50.00%
  ...
  ```
- **CSV** `system_audit_report.csv` listing one row per combination:
  ```
  service,config_sequence,error_hour,total_errors,total_critical,cluster,namespace,app,total_pods,healthy_percent
  auth,"abcd1234ef,ghij7890kl","2025-07-31 13:00",1,1,us-west1,prod,auth,2,50.00
  ```
---

## Suggested Extensions

- Add CLI flags for date, API endpoints, and thresholds.  
- Split each major step into subtasks and run in parallel.  
- Push alerts to Slack/webhook for critical trends or invalid configs.  
