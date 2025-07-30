# SRE Challenge: Kubernetes Pod Status Aggregator

**Scenario Context**  
You receive raw Kubernetes pod information in JSON format from multiple clusters. The goal is to aggregate pod statuses to generate a health report of each service across clusters. This is helpful for global health monitoring dashboards or for sending alerts when services are degraded.

---

## Task Requirements
1. Parse a JSON file (`pods.json`) containing an array of pod metadata from multiple clusters.
2. Each pod includes fields: `cluster`, `namespace`, `app`, `status` (e.g., "Running", "CrashLoopBackOff", "Pending", etc.).
3. Group by `cluster`, `namespace`, and `app`.
4. Compute:
   - Total pods
   - Number of running pods
   - Number of failed pods (`status` not equal to "Running")
   - Percentage of healthy pods

5. Output a CSV file `pod_health_report.csv` with columns:
   ```
   cluster,namespace,app,total_pods,running_pods,failed_pods,healthy_percent
   ```

---

## Input Format (sample JSON)
```json
[
  { "cluster": "us-west1", "namespace": "prod", "app": "payment", "status": "Running" },
  { "cluster": "us-west1", "namespace": "prod", "app": "payment", "status": "CrashLoopBackOff" },
  { "cluster": "us-east1", "namespace": "prod", "app": "payment", "status": "Running" },
  { "cluster": "us-east1", "namespace": "prod", "app": "auth", "status": "Pending" }
]
```

---

## Expected Output / Acceptance Criteria
- CSV output:
  ```
  cluster,namespace,app,total_pods,running_pods,failed_pods,healthy_percent
  us-west1,prod,payment,2,1,1,50.00
  us-east1,prod,payment,1,1,0,100.00
  us-east1,prod,auth,1,0,1,0.00
  ```

- Healthy percent = (running_pods / total_pods) * 100 rounded to two decimal places

---

## Suggested Extensions
- Highlight groups with healthy_percent < 75.00
- Add command-line filters for specific namespaces or clusters
- Output summary in JSON format for API usage
- Visualize using a pie/bar chart

