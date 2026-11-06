# GalaxyMMO Session Handoff

Use this file as the canonical restart point when continuing work in a new ChatGPT conversation. The live branch is authoritative; this file is a checkpoint, not a substitute for checking GitHub.

## Current repository state

- Repository: https://github.com/ViViD420/GalaxyMMO
- Active branch: `development/foundation-hardening`
- Base branch: `main`
- Pull request: https://github.com/ViViD420/GalaxyMMO/pull/1
- PR state at this checkpoint: open, Draft, not merged. Do not merge without the owner's explicit approval.
- This handoff must be refreshed to the exact live commit after the current work is committed.
- Upstream Core3 source pin audited: `403893d9b9f8e6fa712fbb3cb1fcd8f0fe45bb79`
- Core3 build status: not yet built by GalaxyMMO.
- Existing CI validates Python tooling, protocol metadata, and unit tests; it does not build Core3 or Unreal.

## Project direction

GalaxyMMO is an original open-world sandbox MMORPG using Unreal Engine 5 + C++ for its planned client and SWGEmu Core3 as the intended server foundation. Preserve Core3's existing working systems wherever possible. Prefer configuration, data, Lua, and supported extension points. Make only the smallest necessary Core3 changes. Keep GalaxyMMO client-facing contracts separate from Core3 internals until an adapter strategy is proven.

- Do not assume the UE5 client can speak the Core3 protocol directly.
- Do not duplicate Core3 account, character, inventory, persistence, or world-simulation systems without proving a need.
- Evaluate an adapter/gateway only after the relevant Core3 lifecycle and transport behavior is traced; in-process versus separate-process remains undecided.
- Keep simulation and persistence server-authoritative.
- Do not merge the PR, rewrite Core3 subsystems, claim a build passed without evidence, or include proprietary client binaries, extracted assets, archives, art, audio, or data.
- Verify the exact upstream license at the pinned revision before copying, modifying, or distributing Core3 code. Preserve upstream notices.

## Work completed

- Foundation architecture, ADRs, protocol manifest, validator, tests, CI, Core3 build baseline, and checkout verifier.
- Core3 source reconnaissance for login/zone/session/character/scene-ready/movement.
- **Core3 reuse milestone:** `docs/CORE3_REUSE_INVENTORY.md` and expanded `docs/CORE3_FEATURE_REUSE_MATRIX.md` now map Core3's existing server systems to GalaxyMMO reuse decisions, source paths, representative APIs, and remaining verification gates.
- Important finding: Core3 inventory behavior is distributed across SceneObject containment/slot APIs, PlayerManager inventory/trade APIs, and ObjectManager persistence; there is no single standalone inventory manager established by this source review.
- Latest completed project commit before this checkpoint update: to be filled with the current commit after push.
- The reuse inventory is source-level evidence only. No Core3 or Unreal build/runtime verification has been completed.

## Core3 reuse findings

At inspected upstream revision `403893d9b9f8e6fa712fbb3cb1fcd8f0fe45bb79`, existing reuse candidates include:

- Zone orchestration and manager lifecycle.
- Object creation, cloning, persistence, recursive persistence, and deletion.
- Scene-object containment, equipment slots, world placement, zone transfer, and broadcast operations.
- Player/character lifecycle, progression, experience, online state, waypoints, quests, social state, and trade handlers.
- Per-session/per-object ordered task execution.
- Combat resolution and duel handling.
- Crafting schematic, assembly, experimentation, and crafted-value APIs.
- Resource spawning, survey, sampling, harvesting, and resource power accounting.
- Loot, chat/mail/rooms, groups/guilds, missions, auction/vendor workflows, and space/ship systems.
- Spatial indexing structures (octree/quadtree and close-object structures).

Still requiring deeper source audit and runtime verification:

- Credential protection and end-to-end authentication/session handoff.
- Reliability, sequencing, fragmentation, compression, and transport security.
- Object create/destroy, baselines/deltas, interest management, and bandwidth.
- Movement acceptance, validation, correction, and coordinate semantics.
- Inventory/trade/auction/loot atomicity and anti-duplication behavior.
- Persistence transaction boundaries, crash consistency, and reconnect recovery.

## Current next steps

1. Inspect live branch head, PR head/state, and exact-SHA CI at the start of every continuation; never overwrite concurrent work.
2. Obtain a clean Linux environment or remote workstation and check out Core3 separately at the pinned commit.
3. Record actual toolchain/dependency versions and attempt the unmodified upstream debug build.
4. Continue source audit on transport protection/reliability, replication lifecycle, movement validation, persistence transactions, and reconnect.
5. Build a narrow adapter proof of concept only after the build baseline and audit establish the correct boundary.
6. Unreal Engine client work remains a later milestone; this repository does not yet contain a playable UE client, gateway implementation, or integrated Core3 checkout.

## Quick validation commands

From the GalaxyMMO repository root:

```sh
python -m compileall -q tools tests
python tools/validate_protocol.py
python -m unittest discover -s tests -v
python tools/check_core3_checkout.py ../Core3
```

The last command requires a separate, clean Core3 checkout at the audited commit. Passing these Python checks does not establish that Core3 or Unreal builds.

## Restart instruction

When the user says:

> **Resume GalaxyMMO from the handoff checkpoint.**

First read this file and inspect the live GitHub branch, PR, and CI state. Use the live repository as source of truth if it has advanced beyond the SHA recorded above. Continue from the next unfinished step, commit completed work to `development/foundation-hardening`, and report the exact commit SHA and actual CI status. Never overwrite concurrent changes or merge without explicit approval.
