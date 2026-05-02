# Secure Connector Public Boundary

## Purpose

This document explains Secure Connector at a product level without publishing the lock design.

The public docs explain ingredients, principles, safety checks, and outcomes. The private product contains exact timing, ratios, protocol details, pairing, auth, and transport implementation.

## What Secure Connector Does

At a product level, Secure Connector:

- connects approved private devices to Nessa
- enables private local model or tool execution where the account and device policy allow it
- reports controlled health and readiness information
- supports private compute for Linked Devices
- fails closed when unavailable

## Public-Safe Behavior Guarantees

Useful public behavior to document:

- users should know when a private device is selected
- unavailable private devices should not silently fall back across privacy boundaries
- device readiness should be visible without leaking secrets
- private generation or model execution should stay private when selected
- errors should be clear enough to fix, but not expose internals

## What We Do Not Publish

Never publish:

- protocol details
- token exchange
- pairing implementation
- launchd or systemd details
- job schema
- retry behavior
- transport secrets
- direct-sideband mechanics
- exact config paths
- auth headers
- heartbeat schema
- worker queue internals
- device trust scoring
- implementation snippets that make cloning or attacking the connector easier

## Public Explanation Pattern

Use product-level language:

- "approved private device"
- "private local compute"
- "readiness checked"
- "fails closed"
- "no silent external fallback"

Avoid implementation language:

- exact process names
- auth header names
- local state paths
- tunnel details
- job payloads
- timing windows

## Why This Boundary Exists

The connector is a trust boundary. Publishing enough detail to clone or attack it would weaken the product and the users it protects.

The public value is the pattern: private user-owned compute can be integrated into a platform responsibly when approval, readiness, policy, observability, and fail-closed behavior are treated as product requirements.
