# Sanitized AAP Example

This example shows a simple Ansible Automation Platform pattern for collecting
OpenShift and application health before a demo, maintenance window, or model
change.

What the playbook does:
- gathers cluster version information
- gathers cluster operator health
- checks one application deployment in a generic namespace
- checks one `InferenceService`
- optionally calls a generic metadata endpoint
- writes one JSON summary artifact for operators to review

Why this is useful:
- it gives you a repeatable "is the platform healthy?" snapshot
- it reduces last-minute demo guesswork
- it can be scheduled from AAP without embedding real credentials in the repo

How to adapt it:
- replace `private-ai-app` with your application namespace
- replace `ai-notebooks` with your notebook or data-science namespace
- replace `amd-unified-memory-llama` with your own `InferenceService` name
- replace `https://chat.example.com/api/meta` with your own public metadata route
- point `output_dir` to a persistent location if you want to keep snapshots

Sanitization notes:
- there are no real hosts, routes, credentials, or inventory entries here
- the playbook is meant to be run from `localhost` or an AAP execution environment
