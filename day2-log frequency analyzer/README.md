🧠 Objective:
You’re given a server log file access.log. Each line may contain an IP address. Some lines may be corrupted or missing IPs.

📝 Your Tasks:
Read the access.log file line by line.

Extract all valid IPv4 addresses using regex.

Track how many times each IP address appears.

Ignore lines that don’t contain a valid IP — but count how many were skipped.

Write two outputs:

ip_summary.json: a dictionary of IP → count.

errors.log: number of invalid lines skipped.

🧾 Sample access.log:
pgsql
Copy
Edit
2025-07-19 10:00:01 INFO Connection from 192.168.1.1
2025-07-19 10:00:02 INFO Connection from 192.168.1.2
INVALID LINE NO IP
2025-07-19 10:00:03 INFO 192.168.1.1 disconnected
garbage line
✅ Expected Output ip_summary.json:
json
Copy
Edit
{
  "192.168.1.1": 2,
  "192.168.1.2": 1
}
🪵 Expected Output errors.log:
lua
Copy
Edit
2 invalid lines skipped