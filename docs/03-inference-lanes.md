# Inference Lanes

## Purpose

This document explains Nessa AI inference lanes at an architecture level. It intentionally avoids private routing heuristics, hardware IDs, live IPs, account identifiers, connector internals, and exact model-selection rules.

## Lane Summary

| Lane | Public-safe role | Boundary |
|---|---|---|
| OpenShift / Strix Halo | Cluster-hosted accelerated inference and model-serving experiments | OpenShift governed, validated before promotion |
| Apple Silicon Linked Device | User-approved private compute endpoint | Not an OpenShift worker, not a KServe pod |
| CPU historical baseline | Historical fallback and comparison lane | Useful for baseline and resilience, not all workloads |
| BYO-AI provider | User-controlled external provider option | Explicit user choice only |
| Fail-closed private route | Privacy protection behavior | No silent external fallback when privacy forbids it |

## OpenShift / Strix Halo Lane

The Strix Halo lane represents high-memory local accelerated inference hosted as part of the OpenShift platform.

Public-safe lessons:

- unified memory can materially change what local inference can do
- benchmark claims need repeatable proof
- GPU fit is not the same as production readiness
- model-cache storage benefits from local high-throughput storage
- OpenShift placement and resource requests matter

This repo does not publish live node names, live storage object names, private labels, or production route details.

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
