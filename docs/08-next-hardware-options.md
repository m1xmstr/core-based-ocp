# Next Hardware Options

This document is intentionally forward-looking. Only one hardware path in this repository is fully validated in production today: the addition of a single AMD Strix Halo worker. Everything else below should be read as strategic analysis, planning guidance, or partial evaluation rather than a claim of identical hands-on validation.

## Decision framework
When evaluating the next hardware move, we found it helpful to score each option across six questions:

1. How much usable model memory does it really provide?
2. How cleanly does it fit an OpenShift-centric operating model?
3. How much new driver or runtime risk does it introduce?
4. Does it help first-token latency, sustained throughput, or both?
5. What does it do to power, noise, and cooling?
6. Does it improve the platform enough to justify its cost over one more Strix Halo-class node?

## 1. NVIDIA GB10 / Project DIGITS class systems
### Why it is interesting
The GB10 concept is compelling because it promises:
- `128 GB` unified memory class behavior
- strong Blackwell-era inference performance in a desk-friendly form factor
- enough headroom for very large models relative to its size

### Estimated role
For a private AI platform, a GB10-class system could plausibly become:
- a premium inference appliance
- a dedicated large-model lane
- a supplemental endpoint before it becomes a full cluster-serving node

### Pros
- potentially excellent performance density
- strong large-model upside
- compact deployment profile compared with rack GPU servers

### Cons
- NVIDIA ecosystem lock-in
- probable CUDA-centric assumptions throughout the stack
- unclear operational maturity for OpenShift-first homelab use at the time of writing

### Status
**Theoretical.** This repo has not validated a GB10-class system directly.

## 2. NVIDIA RTX 5090-class workstation
### Why it is interesting
A 5090-class workstation is attractive because it offers:
- top-end consumer GPU performance
- broad toolchain familiarity
- a much more common path for AI tooling than emerging AMD or Apple-specific inference lanes

### Estimated role
- high-speed local inference lane
- strong candidate for `70B`-class quantized serving if memory fits
- possible replacement for a Strix Halo worker if raw throughput becomes the only priority

### Pros
- strongest consumer-GPU ecosystem support
- broad compatibility with common AI software stacks
- excellent raw speed for supported workloads

### Cons
- discrete GPU memory is still a hard cap rather than unified-memory flexibility
- separate GPU plus PCIe traffic changes the memory-access story
- power, thermals, and acoustics are worse than a unified desktop appliance

### Status
**Theoretical.** Not validated by this repository.

## 3. Apple Mac Studio M4 Ultra class systems
### Why it is interesting
A high-end Mac Studio is compelling as an adjacent compute endpoint because it offers:
- very high memory bandwidth
- large unified memory pools
- excellent acoustics and power efficiency
- strong local inference characteristics for specific runtimes

### Estimated role
- adjacent inference endpoint
- sidecar inference endpoint
- evaluation or benchmark node
- not a direct OpenShift worker replacement in a conventional x86 cluster

### Pros
- outstanding performance-per-watt
- unified memory helps with larger models
- very low operational friction as a desktop system

### Cons
- ARM architecture changes how it fits the broader platform
- it is not a standard CoreOS/OpenShift worker target in the same way as x86 hardware
- better treated as adjacent capacity than as a direct cluster-node substitute

### Status
**Theoretical as a primary path, partially validated as an adjacent inference endpoint pattern.**

## 4. NVIDIA DGX Station or DGX-class platform
### Why it is interesting
A DGX-class machine is what you buy when you want to remove most model-size constraints.

Potential upside:
- multi-GPU parallelism
- large aggregate memory capacity
- enterprise acceleration story with broad ecosystem support

### Pros
- strongest runway for multi-model or high-concurrency inference
- can support much larger model classes than this repository currently targets
- enterprise credibility is obvious

### Cons
- `~$50,000-150,000` class pricing is outside normal homelab or small-team budgets
- power, thermals, and cooling become a different operational category
- you are no longer solving the same problem as this repository

### Status
**Theoretical.** Included for comparison, not as a practical recommendation for most readers.

## 5. Multi-node Strix Halo cluster
### Why it is interesting
This is the most natural extension of the validated path in this repo.

Instead of jumping ecosystems, you:
- add two or three more units similar to the existing AI worker
- retain a familiar operating model
- explore tensor-parallel or workload-sharded serving across nodes

### Pros
- familiar hardware and runtime path
- likely best continuity with the existing reference architecture
- scales capacity without abandoning what already works

### Cons
- inter-node latency becomes relevant for more advanced parallel serving patterns
- you still depend on an ecosystem path that is less standardized than mainstream NVIDIA/CUDA deployments
- cluster economics remain better than DGX, but still meaningful

### Status
**Partially tested.** This repository validates the first unit strongly, but not the multi-node tensor-parallel scale-out story.

## Recommendation
For home labs and small teams in 2026, the recommendation from this program is straightforward:

1. Stabilize the cluster you already have.
2. Add one strong dedicated AI worker.
3. Exhaust the value of that design before chasing exotic hardware.
4. If you need more, add another Strix Halo-class node or evaluate GB10-class systems when they mature.

The strongest practical advice is this: do not buy hardware to compensate for weak platform discipline. Buy hardware after the platform is good enough that the benchmark deltas will actually mean something.
