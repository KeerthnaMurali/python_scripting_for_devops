# Troubleshooting Practice Scenarios for Meta Production Engineer

## 1. High Disk I/O Latency in File Processing Service

**Context**  
A batch processing job that transforms uploaded files is suddenly taking 3× longer to complete. It's causing a backlog in user-facing features that depend on processed results.

**Questions & Answers**

1. **What tools would you use to confirm that disk I/O is the bottleneck?**  
   - `iostat -x 1 5` to check `%iowait`, `await`, and `svctm`.  
   - `iotop -o` to see per-process I/O usage.  
   - `dstat -dny` or `vmstat 1 5` to correlate I/O wait with system load.  
   - Prometheus metrics: `node_disk_io_time_seconds_total`, `node_disk_read_bytes_total`.

2. **What hypotheses might explain the spike in disk wait time?**  
   - An external batch job or backup started using the same disks.  
   - Hardware degradation: failing disk/controller entering recovery.  
   - Filesystem metadata bloat or fragmentation.  
   - Kernel or driver changes affecting the I/O scheduler.  
   - Network storage throttling (e.g., hitting EBS/NFS IOPS limits).

3. **How would you identify which process or user is causing the I/O pressure?**  
   - `iotop -oPa` to track real-time per-process I/O.  
   - `lsof +D /path/to/workdir` to list open files under the work directory.  
   - `ps -eo pid,user,comm --sort=-%io` to sort processes by I/O usage.  
   - Prometheus container metrics (`container_fs_reads_bytes_total`) filtered by pod.

4. **What short- and long-term mitigations would you implement?**  
   **Short-Term**  
   - Throttle the batch job with `ionice -c2 -n7`.  
   - Isolate I/O in a dedicated volume or cgroup (blkio).  
   - Pause competing cron jobs or backups.  

   **Long-Term**  
   - Provision dedicated SSD-backed volumes for processing.  
   - Autoscale worker nodes with independent storage.  
   - Add alerts on sustained `await > X ms` or queue depth.  
   - Automate SMART health checks and disk replacements.  
   - Optimize filesystem (cleanup temp, defrag) and pin I/O scheduler.

---

## 2. Pod Restart Loop with No Logs

**Context**  
A newly deployed microservice keeps restarting every 45 seconds in a Kubernetes cluster. No logs are produced. It worked in staging.

**Questions & Answers**

1. **What commands would you run to investigate the issue?**  
   - `kubectl describe pod <pod> -n <ns>` to view events, exit codes, restart count.  
   - `kubectl get events -n <ns> --sort-by='.lastTimestamp'` to see recent failures.  
   - `kubectl logs <pod> --previous` to fetch logs from t
