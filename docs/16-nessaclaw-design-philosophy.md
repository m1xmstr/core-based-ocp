# NessaClaw Design Philosophy

NessaClaw is the Nessa product surface for guarded private agent workspaces over OpenClaw-compatible infrastructure.

The public lesson is simple: powerful agent systems should not open with infrastructure dials.

## Front Door Pattern

First paint should show three safe missions and an obvious stop button:

- Run Morning Brief
- Organize Documents
- Smart Home check

These are intentionally small, named, and read-only by default. They help the user understand what the workspace is for before asking them to configure providers, storage, permissions, or tenants.

## Safety Line

The product should say the safety rule plainly:

Nessa runs only the missions you start. You can stop anything with one tap.

That line matters more than another badge. Users relax around powerful software when the brake is visible and the permission model is understandable.

## Advanced Controls

Readiness, private storage, audit, permission center, connected models, connected devices, channels, skills, deployment controls, and instance details still matter.

They should be one tap away behind `Advanced controls`, not removed and not above the fold.

## Boundaries

The public-safe boundary is:

- users interact with Nessa, not a raw OpenClaw route
- owner-only canary and beta-gated rollout are valid safety shapes
- high-impact tools stay locked until explicit approval, preview, audit, and rollback behavior are proven
- the kill switch remains visible and boring
- public docs do not include tenant manifests, gateway tokens, execution recipes, private routes, or high-risk tool enablement steps

## Design Lesson

The best agent UX does not make the user study the control plane first. It gives the user a safe first action, keeps the stop control visible, and keeps the full operator surface available for the moments when it is actually needed.
