# Dili Reliability Control Plane

An independent, Dili-specific DevOps proof of concept for making changes to an ECS/Fargate SaaS platform safer, observable, recoverable, cost-aware, and auditable.

> This repository is an external prototype built from public company/job information. It does **not** claim knowledge of Dili's private infrastructure, source code, incidents, controls, or internal architecture.

## Why this exists

Dili's DevOps role is not just "manage Terraform." The higher-value problem is to make production changes reviewable and repeatable while reducing operational surprises across AWS, ECS Fargate, RDS, S3, IAM, GitHub Actions, observability, backups, and incident response.

This prototype turns those concerns into a deployment contract and an executable promotion gate.

## What it demonstrates

- deployment-safety policy as code
- ECS/Fargate rollback defaults
- observability requirements for logs, metrics, traces, and alerts
- RDS backup / Multi-AZ / PITR / deletion-protection checks
- least-privilege IAM guardrails
- managed-secrets and image-scanning gates
- backward-compatible database migration policy
- service cost-budget warnings
- evidence generation tied to a commit and actor
- Terraform static validation in GitHub Actions

## Architecture

```text
PR / release
   |
   v
Deployment Contract (JSON)
   |
   v
Reliability Policy Engine
   |---- rollout safety
   |---- observability
   |---- backup / DR
   |---- IAM / secrets / image security
   |---- DB migration rollback safety
   |---- cost budget
   |
   +---- FAIL -> block production promotion
   |
   +---- PASS -> evidence.json -> deploy stage
                                  |
                                  v
                       ECS Fargate reference pattern
                       circuit breaker + rollback
```

## Example production contract

See `examples/production-api.json`.

The contract represents the minimum operational assertions a production service should satisfy before promotion. In a real implementation, these values should increasingly be discovered from AWS and telemetry rather than manually asserted.

## Policy catalogue

| Area | Example controls |
|---|---|
| Reliability | >=2 prod tasks, safe deployment capacity |
| Deployment | circuit-breaker rollback, startup grace |
| Observability | structured logs, metrics, traces, alerts |
| DR | RDS retention, Multi-AZ, PITR, deletion protection |
| Security | no wildcard IAM, managed secrets, image scanning |
| Database | backward-compatible migration strategy |
| Cost | projected spend vs service budget |

Hard failures return exit code `1`, allowing CI to block promotion. Warnings reduce the control score but do not automatically block deployment.

## Run locally

```bash
python -m src.dili_control_plane.cli examples/production-api.json --evidence evidence.json
```

Run tests:

```bash
pip install pytest
pytest -q
```

## GitHub Actions

`.github/workflows/ci.yml` runs:

1. Python policy tests.
2. The production deployment contract gate.
3. Evidence artifact generation.
4. `terraform fmt` and `terraform validate`.

The workflow file is not proof that a particular GitHub Actions run has succeeded; check the current repository run status separately.

## Terraform reference

`terraform/modules/service` demonstrates an ECS Fargate service with:

- private networking
- 100% minimum healthy capacity
- 200% deployment maximum
- ECS deployment circuit breaker
- automatic rollback
- load balancer attachment

It intentionally does not provision a complete VPC/RDS/S3 production system. The goal is to show the rollout contract and IaC pattern without pretending a generic sample is Dili's actual architecture.

## Evidence model

A passing or failing policy run writes `evidence.json` containing:

- timestamp
- commit SHA
- actor
- service/environment
- gate decision
- score
- findings

This can evolve into audit evidence for change-management, security, backup, and deployment controls.

## Production evolution

The next version should stop trusting declarative booleans and inspect real systems:

- AWS ECS API for desired/running tasks and rollout state
- CloudWatch and OpenTelemetry for logs, metrics, traces, SLOs
- RDS API for backup retention, Multi-AZ, PITR, deletion protection
- IAM Access Analyzer / policy simulation for privilege checks
- ECR/Inspector for image vulnerability results
- AWS Cost Explorer / CUR for per-service spend and anomalies
- GitHub deployment environments for protected production promotion
- automated database migration compatibility checks
- backup restore exercises, not only backup existence
- canary/progressive delivery with rollback tied to service health

## Dili-specific fit

The public Dili product processes compliance-critical payroll, regulatory, and project data. That makes operational correctness more than availability: releases need to be observable, recoverable, reviewable, and traceable. A change that silently corrupts a payroll interpretation or blocks an audit workflow can be more damaging than a visibly failed request.

This is why the prototype combines deployment safety with evidence, DR, IAM, migration safety, and observability rather than treating them as separate checklists.

## 30 / 60 / 90 framing

- **30 days:** architecture inventory, deployment-path mapping, incident review, SLO/alert baseline, backup/RTO/RPO review, top cost drivers.
- **60 days:** live AWS-backed gates, richer observability, automated restore/IAM checks, safer staging/preview workflows.
- **90 days:** progressive delivery, automated rollback, service cost budgets, DR exercises, reliability scorecards, compliance evidence automation.

See `docs/roadmap.md` for more detail.

## Repository layout

```text
src/dili_control_plane/   policy engine, models, evidence, CLI
examples/                 sample production contract
tests/                    policy tests
terraform/                ECS/Fargate reference IaC
.github/workflows/        CI + deployment gate
docs/                     architecture and roadmap
scripts/                  demo runner
```

## What this prototype intentionally does not claim

- access to Dili's AWS accounts
- knowledge of Dili's current Terraform state
- knowledge of Dili's incidents, SLIs/SLOs, RTO/RPO, or current spend
- authoritative SOC 1/SOC 2 compliance
- authoritative security assessment
- production-ready cost estimates

Those require internal context and live-system access.

## Author

Rahul H Bhatia
