# Skill — Infrastructure as Code

## Purpose

Declare infrastructure (networking, compute, IAM, monitoring) in versioned templates.

## When to use

- DevOps for environments; Security for IAM review; Cost Optimizer for parameter tuning suggestions.

## Practices

- Modules per environment with variable files; no prod secrets in repo.
- State locking for shared stacks.
