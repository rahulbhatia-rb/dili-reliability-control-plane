from datetime import datetime, timezone
from typing import Dict

def build_evidence(report: Dict, commit_sha: str, actor: str) -> Dict:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "commit_sha": commit_sha,
        "actor": actor,
        "service": report["service"],
        "environment": report["environment"],
        "deployment_gate_passed": report["passed"],
        "control_score": report["score"],
        "control_findings": report["findings"],
    }
