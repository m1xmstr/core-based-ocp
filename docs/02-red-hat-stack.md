# Red Hat Stack

## Purpose

This document explains how Nessa AI uses Red Hat technologies in practical, customer-facing architecture language. It avoids vendor-brochure tone and avoids private TryNessa.com implementation detail.

## OpenShift

OpenShift is the foundation for the private AI platform.

Useful patterns:

- deploy web/API tiers as ordinary OpenShift workloads
- keep state in durable services, not pod-local files
- use routes, services, readiness, and rollout status as first-class release signals
- keep inference, web, background jobs, and storage roles separated enough to debug
- prefer explicit placement and resource requests over accidental scheduling

Public-safe lesson: OpenShift makes private AI operationally boring only when the application respects platform boundaries.

## OpenShift AI

OpenShift AI is the model-serving and model-lab layer.

Useful patterns:

- KServe-style model endpoints for OpenShift-hosted inference lanes
- workbenches for validation, notebooks, and repeatable experiments
- model registry and model-serving concepts for governance
- evaluation gates before promoting model or routing changes

Public-safe lesson: a model that fits in memory is not automatically production-ready. Quality, latency, and failure behavior still need proof.

## OpenShift Virtualization

OpenShift Virtualization is relevant when a private AI platform needs VM workloads beside containers.

Useful patterns:

- run supporting VM workloads near the OpenShift platform
- preserve central operations, networking, and observability concepts
- avoid splitting the platform into unrelated container and VM estates

This repo does not publish live VM topology.

## Ansible Automation Platform

AAP is useful for operational repeatability.

Useful patterns:

- health snapshot jobs
- release readiness checks
- storage and route validation
- demo reset or preflight workflows
- operator-friendly runbooks

Public-safe lesson: automation should prove and summarize platform state, not hide it.

## Event-Driven Ansible

EDA fits event-driven operations and release hooks.

Useful patterns:

- webhook-driven deployment checks
- alert-to-runbook loops
- release milestone events
- product-surface audits

Public-safe lesson: event-driven automation needs selectors, event scopes, and failure visibility. A trigger that fires too broadly becomes noise.

## ODF / Ceph Storage

ODF/Ceph provides durable storage patterns for private AI applications.

Useful patterns:

- durable database storage
- document and artifact storage
- workspace storage for agent surfaces
- log and archive storage
- controlled separation between platform storage and local model caches

Public-safe lesson: model-cache storage and application-state storage are different jobs. Treat them differently.

## RHOAI Evaluation and Validation Concepts

Useful validation concepts:

- compare model quality before route changes
- test latency and response quality under realistic prompts
- keep benchmark methods reproducible
- record what was skipped
- do not promote a model lane from hardware fit alone

## Customer Enablement Framing

This repo is useful for:

- customers evaluating private AI on OpenShift
- Red Hat and OpenShift demos
- AAP and EDA operational examples
- teams comparing CPU, Strix Halo, Apple Silicon, and BYO provider lanes
- builders who want private AI patterns without copying TryNessa.com
