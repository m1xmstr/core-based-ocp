# Cost Analysis

A major point of this architecture is that useful private AI does not require an enterprise GPU budget. It does, however, require honest accounting.

## Hardware cost breakdown
| Component | Cost | Notes |
|-----------|------|-------|
| Compact mini PCs x3 | ~$1,350-1,950 | roughly $450-650 each with memory and storage |
| Corsair AI Workstation 300 | ~$2,800 | primary AI worker |
| Network switch | ~$50-100 | unmanaged gigabit or similar lab switch |
| UPS | ~$100-200 | battery backup for graceful outages |
| **Total hardware** | **~$4,300-5,050** | representative range |

## Monthly operating cost
| Item | Cost / month |
|------|--------------|
| Electricity (~400-600W average) | $30-50 |
| Cloudflare or similar edge layer | $0 on free tier |
| Domain names | ~$2 |
| Search API budget | ~$5 |
| **Total monthly** | **~$37-57** |

## Comparison to cloud
| Hosting Option | Monthly Cost | Notes |
|---------------|-------------|-------|
| This home-lab platform | $37-57 | full control, fixed hardware cost |
| Large cloud GPU instance | $1,000-32,000+ | depends heavily on class and utilization |
| Dedicated A100 provider | $1,000-2,000 | pay-per-hour economics can climb quickly |
| Hosted inference API | $100-500+ | easier start, less control, variable usage cost |

## Interpretation
The exact comparison depends on your traffic pattern, but the directional point is strong:

- a few thousand dollars of up-front hardware can replace a very large recurring cloud bill for a private family or small-team AI platform
- the home-lab route buys control, predictability, and architectural learning
- the cloud route buys convenience and scale before you know whether you need them

For the reference platform documented here, the spending pattern that made sense was:
1. start with affordable compact nodes
2. prove the product and platform discipline
3. add one strong AI worker when the product justifies it
4. hold off on premium GPU-server spend until real usage says it is necessary
