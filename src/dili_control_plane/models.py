from dataclasses import dataclass, field
from typing import List

@dataclass
class DeploymentContract:
    service: str
    environment: str
    desired_count: int
    min_healthy_percent: int
    max_percent: int
    cpu_utilization_target: int
    memory_utilization_target: int
    rollback_enabled: bool
    health_check_grace_seconds: int
    structured_logs: bool
    metrics_enabled: bool
    traces_enabled: bool
    alerting_enabled: bool
    rds_backup_retention_days: int
    rds_multi_az: bool
    deletion_protection: bool
    point_in_time_recovery: bool
    iam_wildcards: List[str] = field(default_factory=list)
    secrets_in_secrets_manager: bool = True
    image_scan_required: bool = True
    migration_strategy: str = "expand-contract"
    monthly_cost_budget_usd: float = 0.0
    projected_monthly_cost_usd: float = 0.0
    change_ticket: str = ""
