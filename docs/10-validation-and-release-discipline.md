# Validation and Release Discipline

## Purpose

This document captures the public-safe release discipline behind Nessa AI. It focuses on evidence habits, not private routes, accounts, tokens, or production topology.

## Core Rule

No claim without evidence.

For Nessa, a feature is not treated as fixed until the relevant path is proved at the right level:

- unit or focused regression test where useful
- staging proof before production
- browser proof for user-facing UI flows
- route/model/provider truth for backend or inference changes
- post-deploy health and logs
- documented limitation when proof is incomplete

## Staging Before Production

Public-safe pattern:

1. Make the smallest responsible change.
2. Run focused local checks.
3. Deploy staging.
4. Prove the exact user or operator path.
5. Promote the exact verified artifact to production.
6. Prove production.
7. Check logs and platform health.
8. Update docs to match reality.

## Exact Digest Promotion

The release mindset is to promote the exact verified image or artifact, not "something similar."

Public-safe lesson:

- staging proves a concrete build
- production receives that same build
- docs record what was actually promoted
- rollback points are documented

Do not publish private registry paths or sensitive image-pull details.

## Browser Proof

Backend proof alone is not enough for visible product flows.

Browser proof matters for:

- main chat
- Learning / Homework Buddy
- documents and uploads
- image generation
- billing or plan gates
- Smart Home status
- NessaClaw
- mobile layout

## Platform Cleanup Checks

Public-safe checks include:

- OpenShift deployment readiness
- problem pods
- ClusterOperator health
- ODF/Ceph health
- route health
- recent error logs
- relevant AAP/EDA hook status
- alerts that are unexpected, not expected watchdog-style alerts

## Inference Warmth

When a run touches inference or routing, validate:

- model lane availability
- response latency where relevant
- route/provider truth
- fail-closed behavior
- no silent privacy fallback

## Documentation Truth

Docs must match live runtime.

If docs and runtime disagree, trust runtime and fix the docs.

## Public Boundary

This repo does not publish:

- real private routes
- account emails
- tokens
- private IPs
- production DB rows
- exact deployment commands with live values
- raw logs containing sensitive data
