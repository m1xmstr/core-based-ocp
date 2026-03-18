# Adding a Strix Halo Worker

This is the crown-jewel upgrade in this repository because it is the point where the platform moved from "a compact OpenShift cluster that can technically host AI" to "a compact OpenShift cluster with a genuinely useful AI-serving lane."

## Why We Chose This Hardware
The dedicated AI worker in this reference architecture is a Corsair AI Workstation 300 built around the AMD Ryzen AI Max+ 395. That choice was deliberate.

What made it attractive:
- `128 GB` of unified memory instead of a small fixed GPU VRAM ceiling
- an integrated RDNA 3.5 graphics path that could still drive real `llama.cpp` acceleration
- a desktop-class form factor and power profile rather than a rack-scale GPU server
- enough CPU and memory headroom to host both heavier inference and supporting model-serving processes
- a cost point around `~$2,800`, which is materially easier to justify than a `>$10,000` GPU server

The most important design insight was this: we did not need the strongest possible accelerator on day one. We needed one node that could carry the heavy prompts cleanly without forcing the rest of the cluster into an accelerator experiment.

## What Problem It Solved
By the time the CPU-only phase stabilized, the remaining bottlenecks were obvious:
- first-token latency was still too slow on long prompts
- multi-page writing was usable as a demo but not pleasant as a product
- larger models either did not fit well or did not deliver good enough responsiveness
- inference pressure and general cluster work were sharing the same compact node pool

A single dedicated AI worker solved those problems more cleanly than trying to stretch three compact nodes into something they were never meant to be.

## Installation and Cluster Integration
### 1. Bare-metal installation
The AI worker was treated as a normal OpenShift worker addition rather than a special sidecar appliance.

High-level sequence:
1. prepare firmware and boot order in BIOS
2. install the OpenShift worker with the same cluster trust and machine lifecycle expectations as other nodes
3. join it as a worker node only
4. keep non-AI workloads off it by preference or policy
5. validate device exposure and runtime behavior before routing any real traffic to it

### 2. BIOS reality
The hardware itself was straightforward, but firmware choices still mattered.

The practical concerns were:
- UMA allocation settings
- secure boot and boot-device order
- making sure NVMe devices landed where the OS and later model-cache layout expected them
- avoiding wishful thinking about "BIOS says X, so Linux will expose X"

### 3. CoreOS and driver reality
This system did not drop into the standard ROCm playbook cleanly.

What mattered most:
- the GPU identified as `gfx1151`
- that path was not in the mainstream ROCm support list used in many default guides
- the validated path ended up being Vulkan RADV rather than standard ROCm-only assumptions

This is important because a lot of AI infrastructure guides gloss over the phrase "GPU support" as if it were a single boolean. It is not. You need to validate the exact runtime path that actually works on your chosen OS and kernel.

## Kernel and Memory Tuning
Representative parameters used in the validated environment:

```text
amdttm.pages_limit=27648000
amd_iommu=off
```

These are not universal defaults. They are part of the tuning story for this hardware class on this operating system path.

### GTT allocation reality
The target was larger than the achieved outcome.

- target: roughly `108 GB` of graphics-usable memory headroom
- achieved practical result: roughly `62 GB` GTT exposed in the tested CoreOS driver path
- root cause: kernel / driver limitation in the current operating environment, not simply a BIOS toggle mistake

That gap matters, but it was still enough to transform the usefulness of the platform.

## Storage Layout and Model Cache
The AI worker shipped with two local NVMe devices.

Final intended layout:
- OS and platform/runtime footprint on one local NVMe path
- model cache on the second `2 TB` NVMe path

Why this matters:
- it keeps large GGUF assets off network-attached storage where possible
- it reduces cold-start penalty and repeated artifact pulls
- it separates model-serving I/O from the rest of the platform storage picture

This was not done perfectly on day one. One of the most honest lessons in the project is that the second NVMe sat underused for too long before it was promoted into an explicit model-cache role.

## What Changed Operationally
Once the AI worker was available, several things changed at the same time:

- heavier prompts could route away from the compact nodes
- larger models became practical
- first-token latency got much better
- streaming stopped feeling like a science project
- OpenShift AI / KServe integration became worth the effort instead of mostly decorative
- the compact nodes could go back to doing compact-node work

That last point is underrated. Hardware improvements are often described as throughput wins. In practice, they are also architecture cleanup wins.

## Performance Results
Representative before/after measurements from this program:

| Benchmark | CPU-only cluster | With Strix Halo |
|-----------|-----------------|-----------------|
| 7B model generation | `8-12 tok/s` | `135-150 tok/s` |
| 14B model | impractical | `40-60 tok/s` |
| First token | `4-10s` | `0.3-0.7s` |
| Story (2 pages) | `27.9s` | `7.3s` |
| Research paper | `19.6s` | `12.3s` |
| Concurrent users | `2-3` | `15-30` |
| Bootstrap | `6-32s` | `42-94ms` |

Representative operational observations under load:
- GPU busy: `97-98%`
- memory in active use: roughly `19 GB` of `124 GB` available in the most common serving path
- local NVMe model cache improved cold-start behavior and repeated model bootstrap overhead

These are production-style measurements, not best-case synthetic lab numbers.

## What Did Not Go as Planned
This hardware was worth it, but it was not magic.

### GTT stayed below the theoretical goal
The practical ceiling remained around `62 GB` in the validated CoreOS path even though the hardware architecture suggested more headroom should be possible.

### ROCm was not the easy path
The common assumption that "AMD GPU" means "standard ROCm recipe" turned out to be too simplistic here.

### Vulkan RADV was the path that worked
That is not a complaint. It is an engineering reality worth naming plainly.

### Runtime selection mattered
Ollama was useful early, but the final, stronger serving path leaned on `llama.cpp` / `llama-server`-style behavior because it gave more direct control and better fit for this deployment.

### The second NVMe took too long to become operationally important
The hardware shipped with the answer to a later scaling problem already installed. The team just had to mature enough operationally to use it correctly.

## Advice for Other Teams
If you already have a stable compact OpenShift cluster and want one meaningful upgrade, this is the pattern to consider.

Recommendations:
- start with one strong AI worker before you try to scale out multiple mixed accelerator nodes
- keep a CPU fallback lane even after acceleration arrives
- treat local model cache storage as a first-class design concern
- validate the exact driver and runtime combination instead of assuming generic support statements are enough
- do not let the AI worker quietly become a storage or random workload dumping ground

## Bottom Line
For 2026-era home labs and small teams, a Strix Halo class system is one of the most compelling price/performance upgrades available for local AI inference. It is not because the hardware is perfect. It is because it changes the user experience enough to matter while keeping the rest of the OpenShift platform sane.
