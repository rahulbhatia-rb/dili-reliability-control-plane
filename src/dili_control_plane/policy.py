from dataclasses import asdict
from typing import Dict, List
from .models import DeploymentContract

SEVERITY_ORDER = {"info": 0, "warning": 1, "error": 2}

def _finding(code: str, severity: str, message: str) -> Dict[str, str]:
    return {"code": code, "severity": severity, "message": message}

def evaluate(c: DeploymentContract) -> Dict:
    findings: List[Dict[str, str]] = []

    if c.environment == "production" and c.desired_count < 2:
        findings.append(_finding("REL-001", "error", "Production service should run at least two tasks."))
    if c.min_healthy_percent < 100:
        findings.append(_finding("DEP-001", "warning", "Deployment may reduce healthy capacity during rollout."))
    if c.max_percent < 150:
        findings.append(_finding("DEP-002", "warning", "Deployment surge headroom is low for zero-downtime rollout."))
    if not c.rollback_enabled:
        findings.append(_finding("DEP-003", "error", "Automated rollback must be enabled."))
    if c.health_check_grace_seconds < 30:
        findings.append(_finding("DEP-004", "warning", "Health-check grace period may be too short for safe startup."))

    obs = [c.structured_logs, c.metrics_enabled, c.traces_enabled, c.alerting_enabled]
    if not all(obs):
        findings.append(_finding("OBS-001", "error", "Logs, metrics, traces, and alerting are all required for production."))

    if c.environment == "production" and c.rds_backup_retention_days < 7:
        findings.append(_finding("DR-001", "error", "Production RDS backup retention must be at least 7 days."))
    if c.environment == "production" and not c.rds_multi_az:
        findings.append(_finding("DR-002", "error", "Production RDS should use Multi-AZ."))
    if not c.deletion_protection:
        findings.append(_finding("DR-003", "warning", "Deletion protection is disabled."))
    if not c.point_in_time_recovery:
        findings.append(_finding("DR-004", "error", "Point-in-time recovery must be enabled."))

    if c.iam_wildcards:
        findings.append(_finding("SEC-001", "error", f"IAM wildcard permissions detected: {', '.join(c.iam_wildcards)}"))
    if not c.secrets_in_secrets_manager:
        findings.append(_finding("SEC-002", "error", "Application secrets must be stored in a managed secrets service."))
    if not c.image_scan_required:
        findings.append(_finding("SEC-003", "error", "Container image vulnerability scanning must gate promotion."))

    if c.migration_strategy not in {"expand-contract", "backward-compatible"}:
        findings.append(_finding("DB-001", "error", "Database migrations must be backward-compatible for safe rollback."))

    if c.monthly_cost_budget_usd > 0 and c.projected_monthly_cost_usd > c.monthly_cost_budget_usd:
        findings.append(_finding("COST-001", "warning", "Projected monthly cost exceeds the declared service budget."))

    errors = [f for f in findings if f["severity"] == "error"]
    score = max(0, 100 - 20 * len(errors) - 5 * len([f for f in findings if f["severity"] == "warning"]))
    return {
        "service": c.service,
        "environment": c.environment,
        "passed": len(errors) == 0,
        "score": score,
        "findings": sorted(findings, key=lambda x: SEVERITY_ORDER[x["severity"]], reverse=True),
        "contract": asdict(c),
    }
