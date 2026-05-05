# Hardware and Model Lab: Mac Primary Plus Linux Companion

This page is the short worked example behind the broader [hardware and model lab](./14-hardware-and-model-lab.md).

The current public-safe Nessa pattern uses two complementary high-memory systems:

- MacBook Pro M5 Max with 128 GB unified memory as the private Apple Silicon Linked Device lane
- Ryzen AI Max+ 395 / Strix Halo class Linux companion with 128 GB unified memory as the OpenShift AI worker lane
- Thunderbolt 5 / USB4 direct sideband as fast lab transport between them

No private hostnames, IP addresses, MAC addresses, link-local addresses, credentials, pairing flows, or production routing rules are published here.

## Why This Pattern Works

The Mac is excellent at private Apple Silicon work:

- OCR and AI Vision
- photo and document-heavy workflows
- MLX / Metal model tests
- private image workflows
- large open-weight experiments where unified memory matters

The Linux companion is excellent at platform work:

- OpenShift scheduling and isolation
- cluster-hosted serving experiments
- model-cache and NVMe-heavy workflows
- repeatable validation under the same operations model as the app
- multi-user service behavior

The Thunderbolt sideband makes the lab feel cohesive. Large artifacts, model files, and validation payloads can move quickly without pretending the direct link is a substitute for product policy.

## Public-Safe Lesson

Small private AI platforms do not need to choose between a workstation and a cluster. A calm architecture can let a Mac stay a user-approved private endpoint while a Linux companion stays governed platform infrastructure.

The important rule is fail-closed truth: if a private lane is unavailable, do not silently relabel another route as that lane.
