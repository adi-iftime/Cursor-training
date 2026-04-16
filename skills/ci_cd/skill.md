# Skill — CI/CD

## Purpose

Define continuous integration and delivery pipelines with gated promotions.

## When to use

- DevOps for build/test/deploy; Tester for test stage integration.

## Practices

- Separate workflows for `dev`, `stage`, `prod` with manual approvals where required.
- Artifact immutability: image digest or wheel hash pinned per release.
