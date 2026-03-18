# Repo Scope and Redactions

## Purpose
This repository exists to share the infrastructure, operations, and platform-engineering lessons from a real private AI application without publishing the product itself. The goal is practical reuse: what hardware was chosen, what OpenShift patterns worked, what failed under load, what improved latency, and what an operator should do differently when building a similar platform.

## Why This Repository Is Sanitized
The underlying application is a private commercial product. The value of that product is not only the infrastructure. It also includes product logic, request routing decisions, tenant handling, safety controls, private automation, and user workflows that are intentionally not disclosed here.

Sanitization is not cosmetic. It is part of the contract of this repo.

## What We Intentionally Do Not Publish
We do not publish:
- real domains, route hosts, DNS records, public URLs, or CDN configuration details tied to the live service
- real cluster names, node names, internal IP addresses, MAC addresses, or home-lab topology identifiers
- OAuth client ids, secrets, API tokens, certificates, bearer values, or credential payloads
- private request-routing heuristics, premium product differentiation logic, or user-specific feature toggles
- internal compute-sharing logic, private connector state, or device-mesh coordination details
- customer data flows, retention logic, or encryption implementation details
- billing logic, account entitlements, or product analytics
- private notebooks, internal dashboards, or live customer screenshots

## What We Do Share
We do share:
- the cluster shape that supported the application
- the CPU-first operating model and its limits
- what changed after adding a stronger AI worker
- practical OpenShift deployment patterns
- storage, PVC, and rollout lessons
- real benchmark numbers in sanitized form
- realistic hardware upgrade guidance
- operational checklists and troubleshooting commands

## Naming Conventions Used Here
This repo uses neutral names such as:
- `private-ai-app`
- `chat.example.com`
- `ai-web`
- `ai-core`
- `ai-inference-gateway`
- `ai-postgres`
- `control-plane-1`
- `ai-worker-1`

These are placeholders. They are designed to be legible and reusable, not to mirror live production identifiers.

## Redaction Rules Applied Throughout
The following replacements were applied or maintained intentionally:
- real application names -> `private-ai-app`
- real domains -> `*.example.com`
- real cluster node names -> `control-plane-*` or `ai-worker-*`
- real internal addresses -> omitted entirely or replaced with RFC1918 examples that are clearly illustrative
- personal email addresses -> omitted, except for explicit attribution in the About or License sections where that attribution is intentional

## How To Use This Repo Safely
Treat the contents as:
- a reference architecture
- an implementation pattern library
- a benchmark-backed lessons-learned package
- a planning guide for your own cluster

Do not treat the YAML or examples as drop-in production assets. You still need to adapt:
- storage classes
- SCC and RBAC posture
- route hosts and certificates
- resource requests and limits
- node selectors and tolerations
- secrets and credential sources

## How To Contribute Without Breaking Sanitization
If you contribute, keep changes:
- generic
- reproducible
- free of production identifiers
- free of secrets
- focused on platform patterns instead of product internals

Good contributions:
- clearer diagrams
- better benchmark methodology
- improved OpenShift manifest examples
- better operations checklists
- well-scoped corrections to hardware or performance guidance

Bad contributions:
- screenshots with live routes or identifiers
- copied production YAML with real names intact
- config dumps that include secrets or account details
