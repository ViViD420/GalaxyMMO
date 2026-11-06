# Core3 Integration Plan

## Objective

Use SWGEmu Core3 as the primary server foundation wherever its existing behavior satisfies GalaxyMMO requirements. The project is not a rewrite of Core3. GalaxyMMO work should extend and adapt it conservatively.

## Working rules

- Pin the exact upstream Core3 commit used for every build and integration test.
- Keep the Core3 checkout separate from GalaxyMMO-owned adapter code.
- Prefer existing Core3 services, object lifecycle, task scheduling, persistence, and gameplay systems over replacements.
- Put new client-facing behavior behind GalaxyMMO-owned interfaces.
- Do not expose Core3 C++ types, object IDs, callback factories, or packet structs as the Unreal client's public contract.
- Treat changes to Core3 core code as exceptional and explain each one in a patch note and test.
- Preserve upstream copyright and license notices. Complete the license review before distributing a modified build.

## Integration topology under evaluation

```text
Unreal Engine 5 client
        |
        | GalaxyMMO versioned client contract
        v
GalaxyMMO gateway / adapter (candidate)
        |
        | Core3-native calls or protocol, selected after proof
        v
SWGEmu Core3 services
        |
        v
Core3 persistence and runtime data
```

The gateway is a candidate boundary, not an implemented or selected transport. It may run in-process only if source and lifecycle analysis proves that is safe; otherwise it may be a separate process. Avoid adding a network hop without a measured reason.

## Integration work sequence

### A. Establish a reproducible upstream baseline

- [ ] Select and pin a Core3 revision.
- [ ] Verify the exact license and required notices at that revision.
- [ ] Record supported OS, compiler, dependencies, database version, and runtime data requirements.
- [ ] Build the unmodified upstream revision in a clean supported Linux environment.
- [ ] Run the upstream-provided tests or smoke checks that are available.
- [ ] Record commands, logs, and outcomes; do not infer success from documentation.

### B. Map reusable Core3 capabilities

For each feature, record the relevant Core3 subsystem, extension point, persistence behavior, and test coverage:

- Account authentication and session lifecycle
- Character creation, selection, and deletion
- Zone entry, scene readiness, and reconnect
- Object creation, destruction, containment, and replication
- Movement and interaction validation
- Inventory, equipment, and item persistence
- Combat, crafting, resource gathering, and progression
- Social systems and chat
- Database migrations and world/runtime data

Classify each as **reuse unchanged**, **configure**, **extend**, **adapt at boundary**, or **minimal core patch**.

### C. Prove the client integration boundary

- [ ] Trace authentication and credential protection end-to-end.
- [ ] Trace session handoff from login to zone.
- [ ] Trace character selection through scene-ready.
- [ ] Trace object create/destroy and baseline/delta replication.
- [ ] Trace movement acceptance, coordinate units, and server correction.
- [ ] Determine transport reliability, ordering, fragmentation, compression, and encryption.
- [ ] Build a small conformance client or gateway test that connects to a disposable test server.
- [ ] Compare gateway translation with Core3 authoritative state; test disconnect and reconnect.

### D. Implement only proven requirements

- Add a GalaxyMMO adapter interface and contract tests.
- Implement one vertical slice before broad protocol work: authenticate, list/select a character, enter a test zone, replicate self and one nearby entity, move, disconnect, and reconnect.
- Keep the initial adapter narrow. Do not mirror the entire Core3 API.
- Add tests for malformed messages, oversized payloads, wrong-session commands, duplicate commands, and reconnect races.
- Change Core3 core code only when an observed requirement cannot be met through existing extension points.

## Change review checklist

Before accepting a Core3 modification:

1. Is the behavior already available in Core3?
2. Can configuration, Lua, data, or an existing callback/service provide it?
3. Can the change live in a GalaxyMMO-owned adapter instead?
4. What exact upstream files must change, and why?
5. What regression test fails before the patch and passes after it?
6. Does the patch preserve persistence, task ordering, thread-safety, and session ownership?
7. Can the patch be rebased cleanly onto the pinned upstream revision?

## Current status

This repository currently contains planning, protocol metadata, and validation tooling. It does not yet contain a Core3 checkout, a gateway implementation, or a running server. The next implementation gate is a clean upstream build and a minimal authenticated-session integration proof.
