# The Core-Only Phase

## Why This Phase Matters
The CPU-only phase is not an embarrassment in this story. It is the foundation. Running the application on compact x86 nodes first forced the platform engineering to become disciplined before acceleration masked poor decisions.

This is the phase where the team learned:
- how much latency was architectural versus purely hardware-bound
- how important PostgreSQL, readiness, and rollout discipline were
- what a real user would tolerate on modest hardware
- when the cluster was ready for a dedicated AI worker

## Baseline Hardware and Serving Reality
The initial cluster used three compact x86 nodes with control-plane and worker roles combined. In practice, that meant the same machines were responsible for:
- the OpenShift control plane
- application pods
- storage responsibilities
- small-model inference and fallback serving

That is viable, but it changes how you think about every pod limit and every rollout.

## What Models Were Practical
In the CPU-only phase, the realistic model envelope looked like this:
- `3B` class models were the comfort zone
- small `7B` experiments were possible but not the best fit for production responsiveness
- quantized CPU-friendly formats mattered
- the model that looked good on a benchmark chart was not always the model that produced the best end-user experience

What that meant operationally:
- small prompts were fine
- summaries were viable
- weather, search-assisted lookups, and short answers worked
- long-form generation quickly exposed latency and concurrency ceilings

## Representative CPU-Only Performance
Representative CPU-only measurements from this program were in the range of:
- `8-12 tok/s` for a `7B` class model on compact-node CPU paths
- `4-10s` to first useful token on heavy prompts
- `20-30s` for multi-page or long-form writing requests
- `2-3` serious concurrent users before the system felt stressed

That does not mean CPU-only OpenShift was a failure. It means it had a clear operating envelope.

## What Worked Well
### 1. Basic product flows worked
The platform could support:
- greetings and short chat
- simple support questions
- weather and current-info flows
- small summaries
- short email drafting
- basic coding assistance

That was enough to validate that the product was real.

### 2. OpenShift immediately added value
Even before acceleration, OpenShift gave the system real production habits:
- repeatable rollouts
- route health checks
- operator visibility
- PVC-backed state
- deployment and HPA discipline
- a clean staging-versus-production story

### 3. Application discipline improved faster than the hardware
This is one of the biggest lessons in the whole project.

The CPU-only phase was where the team fixed:
- route and streaming behavior
- health checks
- resource requests and limits
- database durability
- logging quality
- deployment hygiene

Those gains lasted after faster hardware arrived.

## What Struggled
### Long-form generation
This was the most visible pain point.

Typical failure modes in the CPU-only phase:
- stories and research prompts took too long to feel alive
- long responses were more likely to appear stalled
- the user experience felt worse than the raw throughput number suggested
- concurrency made the problem worse very quickly

### Multi-user concurrency
The CPU-only cluster could handle casual traffic, but heavy simultaneous usage caused:
- longer waits to first token
- more contention between application and inference workloads
- more sensitivity to oversized limits
- a perception that the platform was inconsistent rather than just slow

### Operational headroom
Because the same nodes did both control-plane and worker duty, problems compounded:
- an oversized inference pod was not just an app concern
- bad limits became cluster concerns
- PDB mistakes and drain assumptions were riskier during upgrades
- storage and inference traffic were too close together

## What Broke and How It Was Fixed
### SQLite bottlenecks
SQLite was good enough to get started, then became a real platform problem.

Symptoms:
- long bootstrap spikes
- write contention
- inconsistent perceived responsiveness

Fix:
- migrate to PostgreSQL and keep app truth in a real database

### Streaming perception
Even when a response eventually completed, users judged the system based on time-to-first-token and smoothness of output.

Fixes included:
- route and SSE tuning
- web-worker tuning
- reducing app-side blocking before the first stream tokens reached the browser

### Overcommit and noisy limits
The early phase had more theoretical limits than realistic ones.

Fix:
- right-size CPU and memory based on actual usage
- stop treating every pod as if it needs peak theoretical capacity all the time

## What A Typical User Experience Felt Like
A realistic CPU-only user experience felt like this:
- short prompts: acceptable
- weather and simple utility tasks: good enough
- longer answers: noticeably slower, sometimes frustrating
- multi-page writing: proof-of-concept, not premium
- concurrent sessions: fragile enough that users would notice

That is important because many public AI platform writeups skip the human side and only publish infrastructure diagrams.

## What Monitoring and Logging Were Valuable
During this phase the most useful signals were:
- route health
- pod readiness
- app logs filtered for real errors instead of heartbeat spam
- database latency and bootstrap times
- operator health during upgrades

A CPU-first cluster becomes much easier to trust when operators can tell the difference between normal slowness and a real break.

## Deployment Patterns That Helped
The platform got materially better during this phase by standardizing:
- zero-downtime rollouts
- post-deploy health checks
- log review immediately after rollout
- clear staging/prod separation
- better PDBs and readiness probes

## The Most Important Lesson From The CPU-Only Phase
Start with the platform, not the model.

A CPU-only stage is valuable if it helps you prove:
- the product is real
- the cluster is stable
- the observability is strong
- the deployment discipline is credible
- the database is durable

Then, when you add acceleration, you know exactly what improved and why.
