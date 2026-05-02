# BYO-AI Public Pattern

## Purpose

BYO-AI means a user can choose to connect an external AI provider under their own control. This document describes the concept without publishing provider-key storage logic, account linking internals, fallback heuristics, or provider-specific secret handling.

## Public Concept

BYO-AI is useful when a user intentionally wants:

- a specific external provider
- a model not available in the private stack
- a separate budget or provider account
- an explicit cloud route for a specific task

It should not be used as a silent fallback when the user expected private compute.

## Privacy Principles

- Default to private routes where the product promises private behavior.
- Do not expose provider keys in the browser.
- Do not send private prompts externally unless the user has explicitly chosen that route.
- Make external-provider use visible and understandable.
- Respect family and child-safety settings even when an external provider is selected.

## Control-Plane Pattern

At a public-safe level:

1. User connects a provider through a controlled settings surface.
2. Secrets stay server-side.
3. The browser sees provider status, not raw keys.
4. The request router checks privacy, entitlement, safety, and provider availability.
5. External provider use is explicit and auditable.

## Fail-Closed Expectations

BYO-AI should fail closed when:

- BYO is off
- provider credentials are missing or revoked
- privacy mode forbids external routing
- account policy forbids the external route
- safety policy blocks the request

## What Is Not Published

This repo does not publish:

- provider key storage logic
- account linking implementation
- provider-specific secret handling
- exact fallback heuristics
- provider scoring logic
- quota math
- billing or margin logic
- raw API payloads containing secrets
