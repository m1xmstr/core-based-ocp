# Contributing

## Welcome Contributions

Useful contributions include:

- documentation improvements
- clearer diagrams
- benchmark methodology improvements
- public-safe Red Hat and OpenShift patterns
- public-safe AAP and EDA examples
- sanitized OpenShift manifests
- typo fixes
- link fixes
- plain-language explanations for technical readers

## Contributions Not Accepted

Do not submit:

- secrets, keys, tokens, cookies, private keys, or auth headers
- production topology or private route names
- private IPs or private hostnames
- account emails, user IDs, device IDs, or production database snippets
- Secure Connector internals
- pairing or tunnel mechanics
- requests to expose private routing heuristics
- Learning / Homework Buddy lesson-flow logic
- OCR or AI Vision bypass details
- customer, child, family, or private user data
- attempts to bypass safety gates
- full clone recipes for TryNessa.com

## Public-Safe Review Checklist

Before opening a pull request:

1. Run a secret and private-identifier scan.
2. Replace sensitive values with documented placeholders.
3. Keep examples generic.
4. Avoid route names and live object names.
5. Check that diagrams contain no private topology.
6. Make sure Red Hat product names are used factually.
7. Preserve upstream license notices if referencing or adapting third-party work.

## Style

Write in direct, practical language.

Prefer:

- what was validated
- what tradeoff was learned
- what pattern is reusable
- what limitation remains

Avoid:

- hype
- broad unproved claims
- vendor-brochure language
- implementation secrets
