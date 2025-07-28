## 🛠️ DevOps/SRE Daily Coding Challenge (2025-07-28)

**Topic Focus:**  
Dictionary & data manipulation • Exception handling • File & log parsing • Regex analysis • String/data-type transforms • Arithmetic metrics • Date/time scheduling • CSV & JSON processing

---

### 1. Scenario

Your operations team tracks both patch compliance and incident rates. Each week you collect:

- A **CSV** (`servers.csv`) listing each server’s patch level and last-patch date  
- A **JSON** incident feed (`incidents.jsonl`) where each line is a JSON object recording an incident’s timestamp, server ID, and severity  
- A plain-text **syslog** (`syslog.log`) for each server recording restart events  

You need a tool to correlate patch lag with incident frequency, flag at-risk servers, and schedule follow-up checks.

---

### 2. Task Requirements

Write a Python script `patch_incident_report.py` that:

1. **Reads** three files **line-by-line**:  
   - `servers.csv` columns:  
     ```csv
     server_id,patch_version,last_patch_date
     ```  
     (`last_patch_date` in `YYYY-MM-DD`)  
   - `incidents.jsonl`: each line is a JSON object  
     ```json
     {"timestamp":"2025-07-27T14:23:00Z","server_id":"srv-01","severity":"critical"}
     ```  
   - `syslog.log`: plain-text lines like  
     ```
     2025-07-27T15:00:12 srv-01 systemd[1]: Restarted web.service.
     ```
2. **Parses & validates** input formats:  
   - **CSV** via `csv.reader`; parse `last_patch_date` with `datetime.strptime`  
   - **JSON** via `json.loads`; parse `timestamp` into a `datetime`  
   - **Syslog** via `re` to extract `timestamp` and `server_id`; skip malformed lines  
3. **Handles exceptions**:  
   - Missing file → output JSON `{"error":"…"} ` and exit non-zero  
   - Malformed CSV/JSON/syslog lines → skip & tally counts (`malformed_csv`, `malformed_json`, `malformed_syslog`)  
4. **Aggregates** per `server_id`:  
   - `days_since_patch` = `(today.date() - last_patch_date).days`  
   - `incident_count` in the **last 7 days**  
   - `restart_count` in the **last 7 days**  
5. **Computes** a **risk score**:  
   ```python
   risk_score = days_since_patch * (1 + incident_count/10) + restart_count * 2
#### Identify flagged servers  
- Identify `flagged_servers` where `risk_score > 30`

#### 6. Schedule a reminder if any server is flagged  
- **Compute next review** = 3 days after today  
- **Print:**
  ```plaintext
  Reminder: 2 servers flagged. Next review at 2025-07-31T12:00:00Z

## Expected output
```json
{
  "generated_at": "2025-07-28T12:00:00Z",
  "servers": {
    "srv-01": {
      "days_since_patch": 10,
      "incident_count": 4,
      "restart_count": 2,
      "risk_score": 33.0
    },
    "srv-02": { … }
  },
  "flagged_servers": ["srv-01","srv-05"],
  "malformed_csv": 1,
  "malformed_json": 2,
  "malformed_syslog": 3
}

```