# Architecture

The prototype separates **desired deployment intent** from **promotion policy**.

1. Engineering supplies a versioned deployment contract.
2. CI evaluates reliability, rollout, observability, DR, IAM/security, database-migration, and cost policies.
3. A failed hard control blocks promotion.
4. A passing run emits machine-readable evidence tied to the commit and actor.
5. Terraform provides the reference ECS/Fargate service pattern with circuit-breaker rollback and private networking.

Production evolution would integrate AWS APIs, CloudWatch/OpenTelemetry telemetry, RDS backup state, IAM Access Analyzer, ECR/Inspector results, deployment canaries, and incident/SLO data instead of trusting declared booleans.
