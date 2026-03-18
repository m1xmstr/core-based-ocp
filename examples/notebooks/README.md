# Sanitized Notebook Demo Example

This folder contains a small notebook-friendly demo pattern for Red Hat
OpenShift AI or any Jupyter environment that can reach your application and a
KServe endpoint.

What the script demonstrates:
- calling a public metadata endpoint for the app
- calling a cluster-local KServe endpoint
- timing both calls
- writing a human-readable markdown summary artifact

Why keep it simple:
- the point is repeatable demos, not notebook complexity
- operators can use this as a smoke test before a customer call
- the script is generic enough to adapt to different models and namespaces

How to adapt it for your environment:
- set `APP_META_URL` to your application's public metadata endpoint
- set `KSERVE_URL` to your cluster-local or exposed `InferenceService` URL
- set `KSERVE_MODEL` to a model label your serving stack expects
- run it inside a notebook image that has network access to both endpoints

Sanitization notes:
- no real model paths, namespaces, domains, or cluster identifiers are included
- the sample output directory is local to the notebook session
