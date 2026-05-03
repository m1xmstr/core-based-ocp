# Inference Lanes

## Purpose

This document explains Nessa AI inference lanes at an architecture level. It intentionally avoids private routing heuristics, hardware IDs, live IPs, account identifiers, connector internals, and exact model-selection rules.

## Lane Summary

| Lane | Public-safe role | Boundary |
|---|---|---|
| OpenShift / Strix Halo | Cluster-hosted accelerated inference and model-serving experiments | OpenShift governed, validated before promotion |
| Apple Silicon Linked Device | User-approved private compute endpoint for OCR, AI Vision, image workflows, and high-memory model tests | Not an OpenShift worker, not a KServe pod |
| CPU historical baseline | Historical fallback and comparison lane | Useful for baseline and resilience, not all workloads |
| BYO-AI provider | User-controlled external provider option | Explicit user choice only |
| Fail-closed private route | Privacy protection behavior | No silent external fallback when privacy forbids it |

## OpenShift / Strix Halo Lane

The Strix Halo lane represents high-memory local accelerated inference hosted as part of the OpenShift platform.

In this reference architecture, the Strix Halo system is a Ryzen AI Max+ 395 class machine with 128 GB unified memory. Its most important job is not being the only fast machine in the lab. Its job is being a real OpenShift worker that can carry AI workloads under platform governance.

Public-safe lessons:

- unified memory can materially change what local inference can do
- benchmark claims need repeatable proof
- GPU fit is not the same as production readiness
- model-cache storage benefits from local high-throughput storage
- OpenShift placement and resource requests matter

This repo does not publish live node names, live storage object names, private labels, or production route details.

### Why Strix Halo works well as the cluster lane

The Strix Halo lane is strong when the request needs:

- cluster-hosted model serving
- predictable service endpoints
- multi-user request handling
- local model-cache behavior
- OpenShift AI / KServe-style experiments
- controlled placement away from compact control-plane nodes

This is the lane for turning "local AI" into platform infrastructure.

## Apple Silicon Linked Device Lane

Apple Silicon Linked Devices are private, user-approved compute endpoints governed by Nessa.

Public-safe references:

- M3 Max is an earlier Apple Silicon reference point
- M5 Max with 128 GB unified memory is the current high-memory Apple Silicon reference point

Important boundary:

Apple Silicon Linked Devices are not OpenShift workers and are not KServe pods. They are private linked compute endpoints controlled by Nessa policy, user approval, readiness checks, and fail-closed behavior.

Public-safe lessons:

- unified memory matters for larger local models
- private sideband or local transport can help latency and reliability
- explicit linked-device failures must fail closed
- selected premium labels must not silently fall back to unrelated models
- readiness and route truth should be visible to users

### Where Apple Silicon excels

The Apple Silicon lane is strongest when the request benefits from:

- OCR and AI Vision
- document/photo understanding
- MLX / Metal-optimized model execution
- private image-generation experiments
- high-memory local reasoning tests such as GPT-OSS 120B class models
- fast local iteration when the approved device is available

In product terms, this is why the MacBook Pro M5 Max lane became especially important for worksheet, document, photo, and vision-heavy workflows.

## Strix Halo vs M5 Max

| Question | Strix Halo OpenShift worker | M5 Max Linked Device |
|---|---|---|
| Is it part of the OpenShift cluster? | Yes, worker-node pattern | No, private Linked Device pattern |
| Best serving role | cluster-side local inference | private endpoint inference |
| Strongest workloads | text inference, GGUF testing, KServe-style serving, multi-user service behavior | OCR, AI Vision, MLX/Metal, image workflows, high-memory reasoning tests |
| Operational model | node placement, rollout discipline, model-cache storage, cluster health checks | user approval, readiness, fail-closed routing, device health truth |
| Runtime emphasis | Ollama where it wins, `llama.cpp` / `llama-server` where control matters | MLX/Metal, Apple Silicon optimized builds, selected GGUF paths |
| Public-safe lesson | local AI can be governed like platform infrastructure | private compute can be powerful without becoming cluster infrastructure |

See [14-hardware-and-model-lab.md](./14-hardware-and-model-lab.md) for the larger hardware and model-validation story.

## Ollama, llama.cpp, and MLX

The Nessa model lab uses multiple runtimes because the right runtime depends on the workload:

- Ollama is useful for fast iteration, simple local serving, and practical production lanes when it wins live tests.
- `llama.cpp` / `llama-server` are useful for lower-level control, GGUF experiments, OpenShift/KServe-style deployment patterns, and local NVMe model-cache discipline.
- MLX / Metal are the strongest fit for Apple Silicon text, vision, and image workflows.

This repo intentionally avoids declaring a universal winner. The product rule is evidence-based routing: test the model on the real lane, compare it with the current lane, and promote only after proof.

## CPU Historical Baseline

The original CPU-first phase is useful because it explains what breaks first:

- longer latency for heavy prompts
- lower concurrency headroom
- fewer viable model sizes
- greater sensitivity to database and streaming behavior

The CPU lane remains useful as a fallback and baseline, not as the only private AI strategy.

## BYO-AI Provider Lane

BYO-AI lets a user connect external providers by explicit choice.

Public-safe principles:

- provider keys are never exposed in browser docs or examples
- BYO routes should be user-selected, not silent
- private-first defaults should remain private
- when BYO is off, private prompts should not leak to external image or text providers

## Fail-Closed Privacy Posture

Fail-closed means that when a private selected lane is unavailable, the platform returns a clear setup or unavailable response instead of silently routing somewhere else.

Examples of public-safe fail-closed expectations:

- selected private device unavailable: explain that the private device is unavailable
- image-capable device missing: explain setup needed
- BYO disabled: do not send to external providers
- premium model label unavailable: do not relabel a fallback as the requested premium route

## What Is Not Published

This repo does not publish:

- exact route scoring
- routing heuristics
- model priority tables
- live model inventory
- connector heartbeat schema
- hardware IDs
- private transport details
- account-specific route behavior
