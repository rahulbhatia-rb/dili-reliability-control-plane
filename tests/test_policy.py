from dili_control_plane.models import DeploymentContract
from dili_control_plane.policy import evaluate

def base_contract(**overrides):
    data = dict(
        service="api", environment="production", desired_count=2,
        min_healthy_percent=100, max_percent=200,
        cpu_utilization_target=60, memory_utilization_target=70,
        rollback_enabled=True, health_check_grace_seconds=60,
        structured_logs=True, metrics_enabled=True, traces_enabled=True, alerting_enabled=True,
        rds_backup_retention_days=14, rds_multi_az=True, deletion_protection=True,
        point_in_time_recovery=True, iam_wildcards=[], secrets_in_secrets_manager=True,
        image_scan_required=True, migration_strategy="expand-contract",
        monthly_cost_budget_usd=1000, projected_monthly_cost_usd=900, change_ticket="T-1"
    )
    data.update(overrides)
    return DeploymentContract(**data)

def test_safe_contract_passes():
    assert evaluate(base_contract())["passed"] is True

def test_wildcard_iam_blocks_promotion():
    result = evaluate(base_contract(iam_wildcards=["s3:*"]))
    assert result["passed"] is False
    assert any(f["code"] == "SEC-001" for f in result["findings"])

def test_unsafe_migration_blocks_rollback():
    result = evaluate(base_contract(migration_strategy="destructive"))
    assert result["passed"] is False
    assert any(f["code"] == "DB-001" for f in result["findings"])
