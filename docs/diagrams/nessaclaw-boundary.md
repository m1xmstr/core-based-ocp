# NessaClaw Boundary Diagram

This diagram shows the public-safe NessaClaw boundary. It does not expose tenant manifests, tokens, raw gateway routes, private canary IDs, or high-risk tool enablement recipes.

```mermaid
flowchart TB
  User["Eligible user"] --> Nessa["Nessa auth and entitlement"]
  Nessa --> Policy["Policy, safety, and approval gates"]
  Policy --> Decision{"Task decision"}
  Decision -->|allowed| Workspace["Private workspace boundary"]
  Decision -->|approval required| Review["Show plan and wait"]
  Decision -->|blocked| Block["Block with explanation"]

  Workspace --> SafeSkills["Safe WebChat and read-only skills"]
  Workspace --> Storage["Account-scoped storage"]
  Workspace --> Audit["Activity audit"]
  Workspace --> Kill["Kill switch"]

  SafeSkills --> Nessa
  Storage --> Nessa
  Audit --> Nessa
  Kill --> Nessa
  Review --> User
  Block --> User
  Nessa --> User
```
