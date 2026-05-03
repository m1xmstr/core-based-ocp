# Known Constraints and Tradeoffs

A useful public repository should not pretend the platform is perfect. This document lists the practical constraints that still shaped the design.

## 1. Compact cluster reality
A three-node compact OpenShift cluster can host a real private AI application, but it has hard limits.

The main constraints are:
- control-plane and worker responsibilities share the same hardware class
- headroom is tighter than on a larger rack environment
- oversized application limits become cluster problems very quickly
- upgrades require more discipline because node drain assumptions matter more

## 2. CPU-first reality
CPU-first inference is real, but it has a narrow comfort zone.

It is best for:
- small models
- short prompts
- bootstrap product development
- baseline operational validation

It is weaker for:
- multi-page writing
- larger contexts under concurrency
- premium first-token latency
- large-model experimentation at scale

## 3. AMD Strix Halo reality
The Strix Halo worker is one of the most interesting parts of this architecture, but it is not plug-and-play in the simplistic sense.

Constraints we had to work around:
- `gfx1151` is not the easiest path in mainstream accelerator documentation
- the validated runtime path leaned on Vulkan RADV rather than a clean standard-ROCm story
- GTT stayed around `62 GB` in the tested CoreOS path instead of reaching the most optimistic theoretical target

## 4. Storage reality
ODF across compact nodes works, but it is still compact-cluster storage.

Observed constraints:
- shared home-lab networking can produce occasional latency spikes
- storage workloads and inference should be separated clearly
- local NVMe model cache is a different problem from durable cluster storage and must be treated that way

## 5. Apple Silicon Linked Device reality
Apple Silicon is excellent for private high-memory endpoint work, especially OCR, AI Vision, MLX/Metal, image workflows, and GPT-OSS 120B class experimentation.

It is not a normal OpenShift worker.

Constraints:
- readiness must be checked before routing
- user approval and trust boundaries matter
- selected private routes must fail closed when unavailable
- a fast Thunderbolt 5 / USB4 sideband helps lab operations but does not replace product policy
- private connector internals and transport mechanics should not be published

## 6. Signal and helper-service reality
Small utility services can have surprisingly important state.

Example lesson:
- Signal CLI looked simple until pod restarts wiped registration state from ephemeral storage
- persistent mounts were required even though the service was not large

The broader point is that helper tooling should be reviewed for state, not just for CPU or memory footprint.

## 7. Networking reality
This architecture ran on home-lab-style networking, not a full datacenter fabric.

That means:
- a few milliseconds of added latency are normal
- heavy inference and storage traffic can interact in ways you would not see on stronger switching
- alert thresholds built for large enterprise networks may need interpretation rather than blind panic

## 8. Internet dependency reality
Even a mostly private AI platform still depends on outside services if you use modern convenience features.

Typical dependencies may include:
- edge DNS or CDN
- OAuth providers
- public search APIs
- outbound package or model fetches

That does not make the platform less private. It means you should be honest about what parts are local and what parts are still attached to external systems.

## 9. Power and acoustics reality
A compact four-node environment with one serious AI worker is still a real piece of infrastructure.

Practical expectations:
- total draw under load can land around `400-600W`
- the AI worker changes heat and fan behavior materially compared with the control-plane mini PCs
- UPS sizing should be based on the whole environment, not just the compact nodes

## 10. Public repo reality
This repository is intentionally sanitized.

It does not publish:
- real cluster names
- real routes or domains
- real secrets
- internal product differentiation logic
- exact production routing algorithms

That is intentional. The goal is to share the architecture and operations patterns without leaking private implementation detail.
