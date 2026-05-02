# Linked Devices Public Pattern

## Purpose

Linked Devices are Nessa's public concept for private user-owned compute. This document describes the pattern without publishing Secure Connector internals or private routing logic.

## Product Concept

A Linked Device is a user-approved machine that can contribute local compute to Nessa where the product and account policy allow it.

Examples of public-safe device classes:

- Apple Silicon laptops or desktops
- high-memory workstations
- family-owned compute devices
- lab or developer machines approved by the owner

## Trust Model

Linked Devices should be explicit and understandable:

- the user approves device participation
- the product shows whether the device is ready
- the product should explain unavailable states
- a device should not be used for another account unless policy explicitly allows it
- private labels should not hide fallback behavior

## Explicit Selection Versus Automatic Routing

Two public patterns are useful:

- **Explicit selection**: the user chooses a device or private lane. If it is not ready, the request fails closed.
- **Automatic routing**: the product may choose a suitable lane when policy allows. It still needs to report route truth and respect privacy settings.

## Fail-Closed Behavior

Linked Device failures should not silently route across trust boundaries.

Good behavior:

- selected device missing: clear unavailable response
- selected model not installed: setup or unavailable response
- selected private image path unavailable: setup guidance
- provider fallback forbidden: no external send

Bad behavior:

- silently using cloud AI under a private device label
- silently using a smaller model under a premium label
- hiding a failed private route behind generic success copy

## Privacy Expectations

Linked Devices should follow these public principles:

- user-owned compute is optional
- private work should stay private when private mode is chosen
- readiness metadata should be minimal and controlled
- logs should not contain user secrets
- device trust should be revocable

## What Is Not Published

This repo does not publish:

- Secure Connector protocol internals
- pairing flow
- auth tokens
- tunnel mechanics
- sideband transfer details
- job queue internals
- heartbeat schema
- device trust scoring
- exact model routing heuristics
- implementation paths or local config paths
