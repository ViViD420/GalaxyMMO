# Core3 Feature Reuse Matrix

This matrix is a living inventory. A feature is not considered reusable merely because a similarly named class exists; its runtime behavior, persistence, security, and integration points must be demonstrated at the pinned upstream revision.

| Capability | Initial disposition | Evidence needed | GalaxyMMO change policy |
|---|---|---|---|
| Login/account authentication | Reuse candidate | Full credential protection, account checks, session handoff, rate limits | Adapt only the client boundary if required |
| Character listing/selection | Reuse candidate | Ownership validation, concurrent login behavior, error paths | Preserve Core3 lifecycle; map to GalaxyMMO contract |
| Zone sessions | Reuse candidate | Session creation, timeout, reconnect, cleanup | Avoid parallel session authority |
| Scene entry/readiness | Reuse candidate | Complete spawn and scene-ready lifecycle | Adapter translates client-facing state |
| Object lifecycle | Reuse candidate | Create/destroy, containment, ownership, visibility | Preserve Core3 object authority |
| Entity replication | Unverified | Baselines, deltas, ordering, interest management, bandwidth | Do not duplicate until traced |
| Movement | Unverified | Coordinate units, validation, correction, speed/teleport rules | Preserve server validation |
| Inventory/equipment | Reuse candidate | Atomicity, capacity, ownership, persistence, exploit checks | Extend through existing operations |
| Combat | Reuse candidate | Damage authority, cooldowns, range, LOS, persistence | Tune/extend rather than replace |
| Crafting/resources | Reuse candidate | Recipe/resource models, randomization, persistence, exploit controls | Prefer data and narrow extensions |
| Social/chat | Reuse candidate | Permissions, moderation, delivery semantics, persistence | Extend with project-owned features |
| Persistence/database | Reuse candidate | Transaction boundaries, schema migrations, recovery, backups | Avoid parallel writes to same state |

## Status vocabulary

- **Reuse candidate:** subsystem exists in the inspected source, but GalaxyMMO has not completed behavioral/build verification.
- **Unverified:** source-level review is incomplete.
- **Verified reusable:** only after clean build and repeatable tests demonstrate required behavior.
- **Needs extension:** existing behavior is sound but a specific requirement is missing.
- **Core patch required:** only after proving no supported extension or adapter can satisfy the requirement.

## Review record

The current source snapshot is documented in [CORE3_RECONNAISSANCE.md](CORE3_RECONNAISSANCE.md). It is not a substitute for a clean build. Update this table with exact source paths, revision, test evidence, and any known limitations as each subsystem is audited.
