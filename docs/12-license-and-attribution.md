# License and Attribution

## Repository License

This repository is licensed under the Apache License 2.0. See [../LICENSE](../LICENSE) and [../NOTICE](../NOTICE).

SPDX identifier: `Apache-2.0`.

The Apache License 2.0 applies only to the public-safe reference architecture materials, examples, diagrams, and documentation in this repository.

It does not publish or license:

- private TryNessa.com product source code
- Secure Connector internals
- production configuration
- tenant logic
- private routing heuristics
- account flows
- proprietary Learning / Homework Buddy implementation
- secrets or credentials
- private infrastructure
- unpublished Nessa operations code

## Nessa AI and TryNessa.com

Nessa AI / TryNessa.com is a private family-focused AI platform.

This repository documents public-safe architecture patterns and lessons learned. It is not the product source code.

## OpenClaw Attribution

OpenClaw is an upstream open-source project: https://github.com/openclaw/openclaw

NessaClaw is Nessa's guarded product surface built around Nessa authentication, entitlement, policy, storage, audit, and safety controls over OpenClaw-compatible infrastructure.

OpenClaw remains upstream/technical attribution where referenced. NessaClaw is the Nessa product/integration surface.

If any OpenClaw MIT-licensed code, documentation, manifests, or examples are copied or adapted into this repository, preserve their original MIT notices and upstream copyright notices. Do not relicense upstream MIT material as Apache-only.

At the time of this document, the repository references OpenClaw conceptually and does not intentionally publish full OpenClaw-derived deployment recipes.

## Home Assistant Attribution

Home Assistant is an upstream open-source smart-home project:

- website: https://www.home-assistant.io/
- GitHub organization: https://github.com/home-assistant
- Core repository: https://github.com/home-assistant/core

Nessa Smart Home uses Home Assistant where practical as a hub and integration model. Home Assistant remains its own project; Nessa does not imply ownership of Home Assistant or its upstream integrations. Home Assistant source code is not republished in this reference repo.

## Red Hat Product Names

Red Hat, OpenShift, OpenShift AI, OpenShift Virtualization, Ansible Automation Platform, Event-Driven Ansible, OpenShift Data Foundation, and related marks are trademarks or registered trademarks of Red Hat, Inc. or its subsidiaries.

Product names are referenced factually to describe architecture patterns. Do not imply Red Hat sponsorship, endorsement, ownership of Nessa, or certification of Nessa AI unless formally approved and separately documented.

## Third-Party Technologies

This reference architecture may discuss public technologies such as:

- Kubernetes
- KServe
- PostgreSQL
- Ceph
- Apple Silicon
- AMD Strix Halo
- Hugging Face
- Home Assistant
- Ollama
- llama.cpp
- MLX
- local model runtimes
- public AI model families

Their names belong to their respective owners. Public references are descriptive, not ownership claims.

## Contribution License

By contributing to this repository, you agree that your contribution may be distributed under the repository's Apache License 2.0 unless a different license is explicitly agreed in writing.

Do not contribute content you do not have permission to publish.
