# KPI Dashboard Spec v1.0

| Metric              | Prometheus‑namn                | Mål     | Larm‑gräns |
|---------------------|--------------------------------|---------|------------|
| Task‑Completion     | `frank_tasks_completed_ratio`  | > 0.90  | < 0.85     |
| Human‑Intervention  | `frank_hitl_ratio`             | < 0.15  | > 0.25     |
| Avg‑Latency (s)     | `frank_task_latency_sec`       | < 600   | > 900      |
| Token‑Usage / task  | `frank_tokens_per_task`        | Monitor | Spike > 20 % |
