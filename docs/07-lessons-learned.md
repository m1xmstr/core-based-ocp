# Lessons Learned

This document is intentionally blunt. The value of a reference architecture is not that it shows clean diagrams. The value is that it tells you what went wrong, what actually mattered, and what improved the system enough for users to notice.

## 1. Start with platform discipline, not model size
The earliest wins were not glamorous.

They were things like:
- cleaner rollouts
- real readiness checks
- quieter, more useful logs
- saner limits and requests
- reliable routes
- fewer hidden state assumptions

The platform got better before the model stack got impressive. That order mattered.

## 2. SQLite is excellent for starting and bad for staying
SQLite let the application get off the ground quickly. It also became a real bottleneck once concurrent use, session state, and background writes increased.

The symptoms were clear:
- bootstrap spikes of `6-32s`
- write contention
- inconsistent perceived responsiveness
- difficulty reasoning about hot paths under load

Moving to PostgreSQL changed the platform immediately:
- bootstrap fell to `42-94ms`
- auth/session operations stopped looking random
- concurrency stopped fighting a single-writer lock
- production behavior became easier to explain

The lesson is not "SQLite is bad." The lesson is "leave SQLite as soon as the app becomes real."

## 3. Gunicorn worker choice changes how streaming feels
SSE streaming is not a cosmetic add-on in an AI app. It is part of the product.

What we learned:
- sync-worker assumptions make streaming feel worse than it should
- thread-capable workers fit concurrent stream delivery better in this pattern
- users judge the app on first token and cadence, not just total completion time

A system can technically respond and still feel broken. That is a product failure, not just a tuning issue.

## 4. Route buffering can quietly ruin streaming
Streaming quality is not just an application concern.

We had to pay attention to:
- OpenShift route behavior
- proxy buffering
- edge/CDN buffering
- `Cache-Control` and no-buffer style headers

If you do not tune the ingress path, you can spend hours optimizing model speed and still ship a UI that appears to freeze.

## 5. Resource overcommit warnings are not theoretical noise
Compact clusters punish optimistic limits.

What went wrong:
- limits were sometimes set to what a workload might like in theory instead of what it used in practice
- this inflated cluster-level overcommit pressure
- drain and upgrade behavior became harder to trust

What fixed it:
- measure real pod usage
- right-size requests and limits
- reserve big footprints only where the runtime truly needs them

This is especially important when control-plane and worker responsibilities live on the same hardware class.

## 6. Signal and other stateful tools need persistent storage even when they seem small
Signal CLI was a good reminder that "small helper service" does not mean "stateless."

What went wrong:
- account registration state lived on ephemeral container storage
- restarts wiped the local account store
- the service looked randomly broken after normal pod lifecycle events

What fixed it:
- mount a dedicated PVC to the exact runtime path the tool actually uses
- verify by restarting the pod and sending another real message

This is a general lesson. Stateful helper tools should be treated like stateful tools, not like optional sidecars.

## 7. Connector auto-update and compatibility should never block routing unnecessarily
Distributed inference and mesh-style donor devices are fragile enough already.

A bad pattern is:
- version mismatch equals hard routing block

A better pattern is:
- true incompatibility blocks
- minor skew is visible as operator information
- routing stays available when the behavior is still safe

This project repeatedly confirmed that operational tolerance beats rigid purity in mixed-device environments.

## 8. Hardware support claims need to be validated on the target OS, not assumed from the vendor page
The Strix Halo worker proved this clearly.

We learned:
- `gfx1151` support stories were more nuanced than marketing or generic blog posts suggested
- Vulkan RADV ended up being the validated path
- GTT behavior on CoreOS did not line up with the most optimistic theoretical expectations

The correct response is not frustration. It is instrumentation, measurement, and honest documentation.

## 9. One strong dedicated AI worker changed more than adding many weak experiments would have
There is a temptation in homelab AI work to add every interesting machine into the serving pool.

In practice, one strong node did more for product quality than many weak experiments because it:
- simplified routing
- improved latency in the prompts users care about most
- reduced interference with compact control-plane nodes
- made the OpenShift AI story more credible

This is one of the clearest lessons in the entire program.

## 10. Upgrades are where architecture tells the truth
Cluster upgrades surfaced the real quality of the environment.

They exposed:
- weak PDBs
- noisy but harmless alerts
- workloads that should not have been on specific nodes
- lingering operator assumptions
- places where cluster stability depended too much on luck

That is a gift. Upgrade stress reveals system truth before users do.

## 11. Alert hygiene matters as much as alerting itself
A permanently noisy console trains operators to ignore it.

The right pattern is:
- fix the root cause when the alert is real
- document accepted constraints when the environment is intentionally imperfect
- silence known-safe historical noise only after evidence says it is safe to do so

An alert that is always firing is just UI debt.

## 12. Test like a real user, not just like an admin
This should not need to be said, but it does.

Admin tests miss:
- guest-flow friction
- follow-up prompt weirdness
- bad perceived streaming
- upgrade prompts in the wrong place
- empty or broken agent workspaces
- factual answers that look fine structurally but are still wrong

The most painful issues in this project were often not infrastructure failures. They were moments where the system behaved in a way a normal user would instantly reject.

## Final lesson
The best pattern in this project was sequencing:
1. stabilize the platform
2. make persistence real
3. make inference fast enough to matter
4. keep logging, routing, and rollout discipline tight
5. document the truth, including what did not go well

That is how a private AI platform becomes trustworthy.
