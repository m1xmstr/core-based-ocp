# Public Scope and Redactions

## Purpose

This repository is the public, sanitized reference architecture for Nessa AI. It is designed to help builders understand the architecture patterns, Red Hat platform integration, validation discipline, and hardware lessons behind a private family-focused AI platform.

It is not a product-source release and it is not a deployment recipe for TryNessa.com.

## Public Documentation Rule

Public docs should explain:

- what was built
- why it was built
- what was validated
- what tradeoffs were learned
- what patterns are useful to other OpenShift and private-AI builders

Public docs should not expose:

- the exact private recipe
- connector internals
- user data
- routing heuristics
- secrets or credentials
- private network details
- proprietary Learning / Homework Buddy flows
- anything that makes cloning Nessa trivial

## Publishing Matrix

| Class | Publish posture | Examples |
|---|---|---|
| Green | Safe to publish | High-level architecture diagrams, Red Hat product integration patterns, validation methodology, hardware comparison approach, high-level Linked Devices concept, high-level BYO-AI concept, high-level OCR / AI Vision safety pattern, Smart Home and Home Assistant public pattern, NessaClaw public positioning, sanitized run summaries, benchmark methods, sanitized results, lessons learned |
| Amber | Publish only after redaction | Config examples, screenshots, route names, logs, topology diagrams, benchmark raw outputs, model lists, OpenShift object names, connector examples, AAP/EDA event examples |
| Red | Never publish | Tokens, keys, passwords, cookies, real IP addresses, private hostnames, user emails, account IDs, production DB rows, Secure Connector protocol details, tunnel mechanics, pairing/auth flows, raw configmaps/secrets, exact routing heuristics, Learning/Homework Buddy lesson logic, OCR/vision bypass details, Smart Home tokens, raw camera URLs, private home topology, internal price or margin math, child/family/private data, full NessaClaw execution recipes |

## Green Content

The repo can publish public-safe material such as:

- conceptual architecture
- product and platform boundaries
- sanitized OpenShift and OpenShift AI patterns
- staging-before-production validation discipline
- exact digest promotion mindset without private registry details
- AAP and EDA operational patterns
- ODF/Ceph storage roles without private topology
- Strix Halo and Apple Silicon lessons at a hardware class level
- public-safe model-lab methodology, Hugging Face model-family evaluation, and runtime comparison at a class level
- Linked Devices as a user-owned compute concept
- BYO-AI as a user-controlled provider concept
- Learning and family-safety principles
- Smart Home as a simple household status pattern, with Home Assistant linked as upstream open-source technology
- NessaClaw as a guarded product surface over OpenClaw-compatible infrastructure

## Amber Content

Amber content must be reviewed before publication:

- YAML examples
- command snippets
- screenshots
- route names
- benchmark outputs
- model inventory
- OpenShift object names
- AAP/EDA event examples
- topology diagrams
- logs
- connector examples

Before publication, replace live details with placeholders such as:

- `<redacted-private-ip>`
- `<redacted-private-hostname>`
- `<redacted-user-email>`
- `<redacted-hardware-id>`
- `<redacted-token>`
- `<redacted-account-id>`
- `<redacted-route>`
- `<redacted-canary-instance>`

## Red Content

Never publish:

- tokens, keys, passwords, cookies, bearer values, auth headers, private keys, or OAuth secrets
- real private IP addresses, live hostnames, internal routes, home network names, VPN details, or sideband transport addresses
- user emails, account IDs, document IDs, session IDs, device IDs, hardware IDs, or production database rows
- Secure Connector protocol details, pairing/auth implementation, token exchange, heartbeat schema, job queue schema, retry behavior, or transport mechanics
- raw configmaps, secrets, production manifests, or private namespace dumps
- exact routing heuristics, premium route rules, model-selection formulas, fallback thresholds, quota logic, or hidden prompts
- Learning / Homework Buddy prompt chains, worksheet parsers, anti-cheat logic, solution heuristics, lesson-state schemas, or proprietary tutor flows
- OCR or AI Vision bypass details, classifier thresholds, hidden prompts, or exact repair heuristics
- Smart Home tokens, raw camera URLs, private home topology, alarm/security device details, and exact home-control recipes
- private model-selection heuristics, exact prompt suites, model-cache paths, or account-specific routing behavior
- child, family, or private user content
- internal cost margin math, billing decisions, or private financial analytics
- full NessaClaw tenant manifests, gateway configuration, tokens, direct task execution recipes, or high-risk tool enablement steps

## Sanitized Naming

Use public-safe names:

- `Nessa AI`
- `TryNessa.com`
- `NessaClaw`
- `OpenClaw-compatible infrastructure`
- `Linked Devices`
- `private-ai-app`
- `ai-web`
- `ai-inference-gateway`
- `ai-worker`
- `example.com`

Avoid live names, private hostnames, personal account identifiers, real device identifiers, or exact route names.

## Contribution Boundary

Contributions are welcome when they improve public understanding without weakening product safety.

Good contributions:

- clearer diagrams
- better benchmark methodology
- public-safe Red Hat/OpenShift patterns
- sanitized examples
- typo and link fixes

Rejected contributions:

- connector internals
- production topology
- secrets or config dumps
- customer/family data
- safety bypass detail
- full clone recipes
