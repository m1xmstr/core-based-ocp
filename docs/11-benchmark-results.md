# Benchmark Results

This document collects representative benchmark numbers from the reference platform. These are not synthetic best-case microbenchmarks run on an otherwise idle lab. They are production-style measurements taken on real hardware with real application behavior and ordinary background cluster activity.

## Methodology notes
- Numbers represent typical observed performance, not peak showcase values.
- Prompts were drawn from real product-style use cases: greetings, weather, long-form writing, research summaries, code generation, and operational assistant tasks.
- The CPU-only figures represent the compact-node serving phase before the dedicated AI worker was added.
- The Strix Halo figures represent the dedicated AI-worker phase after the platform, database, and serving path were stabilized.
- Apple Silicon adjunct figures are included as adjacent-endpoint context where relevant, not as the core cluster-serving baseline.
- Large-model and vision results are treated as lane-validation results, not universal benchmark claims.

## Inference performance
| Model | Device | Quantization | Prompt Eval (tok/s) | Generation (tok/s) | Time to First Token |
|-------|--------|-------------|--------------------|--------------------|-------------------|
| Qwen 2.5 7B | Strix Halo GPU | Q4_K_M | 450+ | 135-150 | 0.3-0.7s |
| Qwen 2.5 7B | Mac M3 Max | Q4_K_M | 300+ | 80-100 | 0.5-1.0s |
| Qwen 2.5 7B | Compact-node CPU path | Q4_K_M | 30-50 | 8-12 | 4-10s |
| Phi-3 mini | CPU fallback | Q4_K_M | 40-60 | 15-20 | 2-5s |
| DeepSeek R1 8B | Strix Halo GPU | Q4_K_M | 350+ | 100-120 | 0.5-1.0s |

## Hardware role comparison

| Lane | Validated role | Practical strength | Not the best fit for |
|---|---|---|---|
| Strix Halo / Ryzen AI Max+ 395, 128 GB | OpenShift AI worker | cluster-side serving, GGUF testing, local NVMe model cache, repeatable benchmarks | acting as a raw desktop-only AI appliance |
| MacBook Pro M5 Max, 128 GB | Apple Silicon Linked Device | OCR, AI Vision, MLX/Metal, private image workflows, GPT-OSS 120B class tests | becoming a normal OpenShift worker |
| Compact cluster nodes | app/data/control-plane baseline | platform services, PostgreSQL, ODF/Ceph, routing, fallback | carrying heavy long-form inference as the primary lane |

## Application benchmarks
| Use Case | CPU-only | Strix Halo | Apple Silicon adjunct |
|----------|----------|------------|-----------------|
| "Hi" response | 1-2s | <0.5s | <0.5s |
| Weather lookup | 2-3s | 1-2s | 1-2s |
| 2-page story | 27.9s | 7.3s | 10-12s |
| Research paper | 19.6s | 12.3s | 15-18s |
| Email draft | 2.97s | 1.99s | 2.2s |
| Code function | 8-15s | 3-5s | 5-8s |
| Gas price lookup | 45s -> 1s after fixes | 1-5s | 1-5s |

## Apple Silicon large-model and vision notes

The MacBook Pro M5 Max lane is included here because it changed what the product could test privately:

- GPT-OSS 120B class model routing was validated on the high-memory Apple Silicon Linked Device lane.
- MLX / Metal paths were the natural fit for Apple Silicon-specific model tests.
- OCR and AI Vision workflows benefited from keeping document/photo work on a private high-memory endpoint when readiness and policy allowed it.
- The product rule remained fail-closed: if the requested Apple Silicon route was unavailable, Nessa did not silently relabel a fallback as the selected model.

This repo does not publish hardware IDs, private route names, private prompt suites, model-cache paths, or connector internals.

## Database migration impact
| Metric | SQLite | PostgreSQL | Improvement |
|--------|--------|------------|-------------|
| Bootstrap | 6-32s spikes | 42-94ms | 300x+ |
| Auth session path | ~5,000ms spikes | <20ms | 250x |
| Concurrent writes | single-writer lock | MVCC | qualitative step change |
| Tables migrated | 38 | 38 | zero schema-loss events |

## Streaming performance
| Metric | Before | After |
|--------|--------|-------|
| First token | 4-10s | 0.3-0.7s |
| Token cadence p50 | batchy / inconsistent | ~21ms |
| Perceived responsiveness | "feels broken" | "feels instant" |

## Infrastructure observations
| Resource | AI worker idle | AI worker under load |
|----------|----------------|----------------------|
| CPU | ~3% | 15-25% |
| Memory | ~19 GB / 124 GB | 40-60 GB / 124 GB |
| GPU busy | 0% | 97-98% |
| NVMe model cache | little activity | up to ~7 GB/s sequential reads |

## Thunderbolt 5 direct sideband

The Strix Halo OpenShift worker and the M5 Max Linked Device were also validated with a high-speed Thunderbolt 5 / USB4 direct sideband.

Public-safe operational result:

- direct sideband throughput was materially better than ordinary LAN transfer in the validated lab
- large model artifact movement and validation payload movement became less painful
- the sideband improved the lab workflow without becoming a blanket routing policy

The public repository intentionally does not publish private interface names, addresses, or route mechanics.

## Interpretation
The most important takeaway is not that every number improved by the same factor. They did not.

The most important takeaway is that the platform crossed a threshold:
- long-form work became viable
- first-token latency became competitive with user expectations
- heavier prompts stopped monopolizing the compact nodes
- the application became much more credible as a daily-use private AI service
- OCR and AI Vision could use the Apple Silicon lane where it fit better than cluster-side serving
- the Strix Halo node gave OpenShift a real AI worker instead of forcing the app cluster to behave like a GPU appliance

That threshold matters more than any one benchmark row.
