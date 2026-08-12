import argparse, json, os, sys
from .models import DeploymentContract
from .policy import evaluate
from .evidence import build_evidence

def main() -> int:
    p = argparse.ArgumentParser(description="Evaluate a Dili-style deployment contract")
    p.add_argument("contract")
    p.add_argument("--evidence", default="evidence.json")
    args = p.parse_args()
    with open(args.contract) as f:
        raw = json.load(f)
    report = evaluate(DeploymentContract(**raw))
    print(json.dumps(report, indent=2))
    evidence = build_evidence(report, os.getenv("GITHUB_SHA", "local"), os.getenv("GITHUB_ACTOR", "local"))
    with open(args.evidence, "w") as f:
        json.dump(evidence, f, indent=2)
    return 0 if report["passed"] else 1

if __name__ == "__main__":
    sys.exit(main())
