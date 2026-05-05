# Hardware and Model Lab

Nessa AI is not only an application pattern. It is also a practical hardware and model-validation program.

This document explains the public-safe architecture story behind two high-memory local AI systems used in the Nessa reference platform:

- an AMD Strix Halo / Ryzen AI Max+ 395 system with 128 GB unified memory, used as an OpenShift AI worker node
- a MacBook Pro M5 Max with 128 GB unified memory, used as a private Apple Silicon Linked Device
- a Thunderbolt 5 direct sideband between the Apple Silicon endpoint and the Linux companion lane for lab artifact movement and validation work

It also explains why the project tests Hugging Face models continuously, why both Ollama and `llama.cpp` matter, and why this path was chosen instead of starting with a rack-scale DGX-style appliance.

This is intentionally sanitized. It does not publish private hostnames, IP addresses, hardware IDs, Secure Connector internals, account routing rules, tokens, secrets, production manifests, or proprietary Learning / Homework Buddy logic.

## The Short Version

The most important architecture decision was not "which machine is fastest."

The important decision was to split the problem into two complementary lanes:

| Lane | Hardware | Best At | Why It Matters |
|---|---|---|---|
| OpenShift AI worker | Strix Halo / Ryzen AI Max+ 395, 128 GB | Cluster-hosted local inference, OpenShift placement, model-serving experiments, repeatable benchmarks | Turns local AI into platform infrastructure instead of a sidecar demo |
| Apple Silicon Linked Device | MacBook Pro M5 Max, 128 GB | OCR, AI Vision, MLX/Metal workloads, GPT-OSS 120B class experimentation, private user-approved compute | Gives Nessa a high-memory private lane that excels at image/document-heavy workflows |
| Compact cluster nodes | Small OpenShift nodes | App, data, storage, operators, baseline fallback | Keeps the platform stable while specialized hardware does specialized work |

This design gives Nessa multiple ways to serve a request without pretending every workload belongs on the same device.

## Strix Halo as an OpenShift AI Worker

The Strix Halo unit is the platform lane.

It is valuable because it can become a real OpenShift worker:

- it participates in normal cluster scheduling and rollout discipline
- it can host accelerated inference services beside the app platform
- it can use local NVMe model cache for large model artifacts
- it can be labeled and isolated for AI workloads
- it can be observed, drained, validated, and promoted through the same operational habits as the rest of the cluster

The system used in this reference architecture is a Corsair AI Workstation 300 class machine built around AMD Ryzen AI Max+ 395 with 128 GB unified memory and a local NVMe layout sized for both OpenShift workloads and future model-cache experiments.

### Where Strix Halo excels

Strix Halo is strongest when the problem is:

- cluster-side text inference
- larger GGUF model testing
- multi-user service behavior
- repeatable model benchmarks
- OpenShift AI / KServe-style serving experiments
- local model-cache storage
- keeping AI work off the compact control-plane nodes

The important practical win is not only token throughput. It is platform cleanliness. Heavy model work stops crowding the compact nodes, and AI serving becomes a schedulable OpenShift capability.

### Strix Halo reality

Strix Halo is powerful, but it is not a generic "all AI frameworks work out of the box" checkbox.

Public-safe lessons from this program:

- exact GPU exposure matters more than marketing names
- ROCm assumptions did not map cleanly to every path we needed
- Vulkan / RADV and GGUF-based runtimes were practical in the validated lane
- local NVMe model cache mattered
- OpenShift resource requests, node placement, and warmup checks mattered
- every model needed real load, latency, and output-quality proof before promotion

## MacBook Pro M5 Max as an Apple Silicon Linked Device

The M5 Max is the private high-memory endpoint lane.

It is not an OpenShift worker and it is not a KServe pod. It is a user-approved Linked Device governed by Nessa policy, readiness checks, and fail-closed routing.

That distinction matters. The MacBook can be excellent at local AI without becoming part of the cluster scheduler.

### Where Apple Silicon excels

In this architecture, Apple Silicon became especially valuable for:

- OCR and AI Vision workflows
- document and photo understanding
- MLX / Metal-optimized models
- high-memory local model experimentation
- private image-generation and image-understanding lanes
- GPT-OSS 120B class linked-device experimentation
- fast interactive testing when the private device is available

Apple Silicon's unified memory and MLX/Metal ecosystem made it a strong fit for vision-heavy private workflows. In product terms, that means worksheet/photo/document requests can stay on a private local lane when policy and readiness allow it.

### GPT-OSS 120B on Apple Silicon

Nessa validated a GPT-OSS 120B class model lane on the high-memory Apple Silicon path.

Public-safe lessons:

- high-memory Apple Silicon can be a practical local test lane for very large open-weight models
- split or nested model artifacts need deliberate model-cache and loader handling
- first load and warmup behavior must be treated as product behavior, not only a lab detail
- the UI and backend must fail closed if the selected large-model lane is unavailable
- successful large-model routing must report the real route instead of relabeling a fallback

The GPT-OSS lane is a good example of Nessa's general model policy: prove the route, prove the model, prove the failure mode, then expose it.

## Thunderbolt 5 Direct Sideband

The Strix Halo OpenShift worker and the M5 Max Linked Device are also connected by a high-speed Thunderbolt 5 / USB4 direct path in the reference environment.

The public-safe point is not the private interface details. The point is the architecture pattern:

- a direct sideband can move model artifacts and validation payloads without relying on ordinary LAN paths
- high-throughput local transfer makes large-model testing less painful
- the sideband helps the lab operate faster without requiring ordinary user traffic to use it by default
- routing policy still matters; a fast cable is not a privacy policy

In practical terms, the direct path made the Strix/M5 pair feel like a cohesive local AI lab instead of two disconnected machines.

## Mac Primary Plus Linux Companion

The current public-safe pattern is:

- MacBook Pro M5 Max, 128 GB: private Apple Silicon primary Linked Device for OCR, vision, MLX/Metal, private image workflows, and large open-weight experiments
- Ryzen AI Max+ 395, 128 GB: Linux/OpenShift companion for cluster-hosted serving, cache-heavy experiments, and platform validation
- Thunderbolt 5 sideband: fast lab transport for artifacts and proof, not a blanket product-routing rule

This is a calm pattern for small private AI teams because it avoids forcing one machine to be everything. The Mac remains a user-approved private endpoint. The Linux box remains platform infrastructure. The direct sideband makes the lab faster without replacing policy, auth, or fail-closed routing.

## Why Not Just Buy a DGX?

DGX-class systems are excellent for teams that need a supported rack-scale NVIDIA AI appliance and have the power, budget, cooling, and operations model to match it.

That was not the first problem Nessa needed to solve.

Nessa needed:

- one compact AI worker that could join OpenShift
- a private Apple Silicon lane for OCR, vision, and high-memory local tests
- routine model evaluation without turning the whole platform into a GPU appliance project
- enough acceleration to make the product feel real
- a cost and power profile that made sense for a private family-focused AI platform
- architecture lessons other builders could reuse

The Strix Halo + M5 Max pattern fit that target better than starting with a DGX-style device. It produced a platform story, not only a benchmark story.

## Hugging Face as the Model Research Layer

Hugging Face is used as a model-discovery and artifact-review layer, not as a blind auto-install source.

The model lab looks for:

- license and redistribution fit
- model family and intended task
- text-only, code, vision-language, image-generation, or embedding role
- quantized formats such as GGUF or MLX-friendly builds
- memory fit on Strix Halo and Apple Silicon
- runtime compatibility with Ollama, `llama.cpp`, MLX, KServe-style serving, or other tested lanes
- safety and product-quality behavior under real prompts

Representative public-safe model families evaluated or tracked in this program include:

| Model family | Public role in the lab | Why it mattered |
|---|---|---|
| Qwen 2.5 / Qwen Coder | fast text, coding, and baseline local inference | strong practical baseline for local serving |
| Qwen VL / Qwen3-VL candidates | OCR, document, and AI Vision exploration | vision-language models are central to worksheets/photos/documents |
| Gemma 4 | private response and local model comparison | useful family of local models for quality/latency tradeoffs |
| DeepSeek R1 distilled models | reasoning-style experiments | helped compare reasoning behavior against latency and fit |
| GPT-OSS 120B | high-memory reasoning lane on Apple Silicon | validated the M5 Max as a serious large-model local endpoint |
| FLUX / MLX image models | private image-generation experiments | Apple Silicon MLX/DiffusionKit builds were a practical local image lane |
| Embedding models | retrieval and document search support | small models can be as important as large chat models |

The public repo does not publish private prompt suites, private eval data, account-specific routing, or model-selection heuristics.

Public model-card examples:

- [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b)
- [Qwen/Qwen3-VL-30B-A3B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-30B-A3B-Instruct)
- [Qwen/Qwen3-VL-30B-A3B-Instruct-GGUF](https://huggingface.co/Qwen/Qwen3-VL-30B-A3B-Instruct-GGUF)
- [google/gemma-4-E4B-it](https://huggingface.co/google/gemma-4-E4B-it)
- [argmaxinc/mlx-FLUX.1-schnell-4bit-quantized](https://huggingface.co/argmaxinc/mlx-FLUX.1-schnell-4bit-quantized)

## Ollama vs llama.cpp vs MLX

The project did not pick one runtime and force every workload through it.

It used the runtime that fit the job.

| Runtime | Where it helped | Why it was used |
|---|---|---|
| Ollama | fast model iteration, simple local serving, operationally convenient cluster routes | useful when it was the fastest stable path for a model family |
| `llama.cpp` / `llama-server` | lower-level control, GGUF experiments, OpenShift/KServe-style serving, local NVMe cache discipline | useful when the team needed more direct control over serving behavior |
| MLX / Metal | Apple Silicon text, vision, and image-generation experiments | best fit for Apple unified memory and the M5 Max local lane |
| KServe / OpenShift AI patterns | governed model-serving lifecycle, workbench validation, model-lab discipline | useful for turning experiments into platform practices |

The lesson is not "Ollama beats llama.cpp" or the reverse. The lesson is that product routing should be evidence-based. If Ollama wins a live benchmark, use it. If `llama.cpp` gives better OpenShift control for a serving experiment, use that. If MLX is the right Apple Silicon path, use MLX.

## Routine Model Validation Loop

The Nessa model-lab loop is intentionally boring:

1. Identify a candidate model from Hugging Face, vendor docs, or project needs.
2. Check license, intended use, model card warnings, and artifact format.
3. Decide likely lane: Strix Halo, Apple Silicon, CPU fallback, OpenShift AI/KServe, or BYO provider.
4. Download into a controlled model cache.
5. Prove it loads.
6. Measure warm and cold behavior.
7. Run product-style prompts: short chat, long writing, code, OCR/vision, safety cases, and failure cases.
8. Compare against the current production lane.
9. Promote only after staging proof.
10. Keep the previous lane available until the new one proves it deserves traffic.

This is the difference between a model zoo and a product platform.

## What This Repo Does Not Publish

This repo does not publish:

- live node names, IP addresses, hostnames, or hardware IDs
- private route selection rules
- Secure Connector internals
- private pairing or transport mechanics
- production configmaps, secrets, tokens, or account data
- private prompt suites or eval datasets
- proprietary Learning / Homework Buddy logic
- exact OCR repair heuristics or bypass details
- raw model-cache paths or private deployment recipes

## Bottom Line

The Strix Halo unit made Nessa's OpenShift cluster a real local AI platform. The M5 Max made private OCR, vision, image, and very-large-model experimentation practical. Thunderbolt 5 made the two systems feel like one high-throughput local lab.

Together they created the architecture this repo is trying to share: private AI is not one machine, one model, or one runtime. It is a disciplined platform that knows which lane should do which job, proves it, and fails closed when the right lane is not available.
