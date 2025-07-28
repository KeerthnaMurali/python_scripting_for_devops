1. Scenario
Your SRE team is consolidating metrics collected from different monitoring agents. Each agent logs a JSON line for every metric event it records. Some agents have older versions that produce malformed or incomplete JSON entries. Your task is to build a reliable collector that:

Ingests raw agent logs

Cleans up partial or malformed entries

Aggregates metrics per host

Generates a single daily summary for alerting and dashboards

2. Task Requirements
Write a Python script summarize_metrics.py that:

Reads a file agent-metrics.log line-by-line (each line is a JSON object).

Parses and validates each line to extract:

host_id (string)

metric_name (e.g., "cpu.usage", "mem.free")

value (float)

unit (optional string, e.g., "percent" or "MB")

timestamp (ISO 8601, e.g. "2025-07-22T04:32:12Z")

Skips and counts malformed JSON or entries missing host_id, metric_name, or value.

For each host_id, aggregate:

Number of valid metrics

List of distinct metric names seen

Average value of "cpu.usage" if present

Outputs a single-line JSON report to stdout:

json
Copy
Edit
{
  "generated_at": "2025-07-22T12:00:00Z",
  "hosts": {
    "host-001": {
      "metrics_count": 28,
      "unique_metrics": ["cpu.usage","mem.free"],
      "avg_cpu_usage": 53.6
    },
    "host-002": {
      ...
    }
  },
  "malformed_lines": 4
}
Use only the Python standard library and stream the file (don’t load it entirely).

