# Linked Devices Pattern Diagram

This diagram is a product-level pattern. It does not describe Secure Connector protocol, pairing, token exchange, heartbeat schema, job payloads, or transport mechanics.

```mermaid
flowchart LR
  User["User"] --> Consent["Approve device participation"]
  Consent --> Device["User-owned private device"]
  Device --> Health["Controlled readiness signal"]
  User --> Request["Request using private compute"]
  Request --> Nessa["Nessa policy and routing"]
  Health --> Nessa
  Nessa --> Ready{"Device ready and allowed?"}
  Ready -->|yes| Compute["Private local execution"]
  Ready -->|no| Fail["Fail closed"]
  Compute --> Result["Result with route truth"]
  Fail --> Guidance["Unavailable or setup guidance"]
  Result --> User
  Guidance --> User
```
