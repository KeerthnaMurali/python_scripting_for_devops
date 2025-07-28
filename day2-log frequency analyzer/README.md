## 🧠 Objective

You’re given a server log file `access.log`. Each line may contain an IP address. Some lines may be corrupted or missing IPs.

---

## 📝 Tasks

1. **Read** the `access.log` file line by line.  
2. **Extract** all valid IPv4 addresses using regex.  
3. **Track** how many times each IP address appears.  
4. **Ignore** lines that don’t contain a valid IP — but **count** how many were skipped.  
5. **Write** two outputs:  
   - `ip_summary.json`: a dictionary of IP → count  
   - `errors.log`: the number of invalid lines skipped  

---

## 🧾 Sample `access.log`

```text
2025-07-19 10:00:01 INFO Connection from 192.168.1.1
2025-07-19 10:00:02 INFO Connection from 192.168.1.2
INVALID LINE NO IP
2025-07-19 10:00:03 INFO 192.168.1.1 disconnected
garbage line
```

---

## ✅ Expected Output `ip_summary.json`

```json
{
  "192.168.1.1": 2,
  "192.168.1.2": 1
}
```

---

## 🪵 Expected Output `errors.log`

```text
2 invalid lines skipped
```