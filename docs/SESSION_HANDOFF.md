# GalaxyMMO Session Handoff

Use this file as the canonical restart point when continuing work in a new ChatGPT conversation. The live branch is authoritative; this file is a checkpoint, not a substitute for checking GitHub.

## Current repository state

- Repository: https://github.com/ViViD420/GalaxyMMO
- Active branch: `development/foundation-hardening`
- Base branch: `main`
- Pull request: https://github.com/ViViD420/GalaxyMMO/pull/1
- PR state at this checkpoint: open, Draft, not merged. Do not merge without the owner's explicit approval.
- Current branch / PR head at this checkpoint: `78bf892341707d349ddf5618e3aa5e6c24f24a95`
- Commit title: `security: tighten manifest and upstream validation`
- Commit tree: `7830090f94d99f4cd032b8cf07cefea9c58c4128`
- Upstream Core3 source pin audited: `403893d9b9f8e6fa712fbb3cb1fcd8f0fe45bb79`
- Core3 build status: not yet built by GalaxyMMO.
- Exact-SHA CI for `78bf892341707d349ddf5618e3aa5e6c24f24a95`: both completed successfully:
  - Push run: https://github.com/ViViD420/GalaxyMMO/actions/runs/42229714378
  - Pull request run: https://github.com/ViViD420/GalaxyMMO/actions/runs/42229724190
- These CI workflows compile Python tooling, validate the protocol manifest, and run the Python unit tests. They do not build Core3 or an Unreal client.

## Project direction

GalaxyMMO is an original open-world sandbox MMORPG using Unreal Engine 5 + C++ for its planned client and SWGEmu Core3 as the intended server foundation. Preserve Core3's existing working systems wherever possible. Prefer configuration, data, Lua, and supported extension points. Make only the smallest necessary Core3 changes. Keep GalaxyMMO client-facing contracts separate from Core3 internals until an adapter strategy is proven.

- Do not assume the UE5 client can speak the Core3 protocol directly.
- Do not duplicate Core3 account, character, inventory, persistence, or world-simulation systems without proving a need.
- Evaluate an adapter/gateway only after tracing the relevant Core3 lifecycle and transport behavior; in-process versus separate-process is not decided.
- Keep simulation and persistence server-authoritative.
- Do not merge the PR, rewrite Core3 subsystems, claim a build passed without evidence, or include proprietary client binaries, extracted assets, archives, art, audio, or data.
- Verify the exact upstream license at the pinned revision before copying, modifying, or distributing Core3 code. Preserve upstream notices.

## Work completed

- Foundation documentation, architecture decisions, protocol manifest, validator, tests, and CI workflow.
- Core3 login/zone/session/character/scene-ready/movement source reconnaissance at the pinned source revision.
- ADR-0003 documenting the Core3 preservation strategy.
- Core3 integration plan and feature reuse matrix.
- Draft authentication/session contract; no auth service or wire protocol has been implemented.
- Pinned Core3 build baseline and read-only checkout verifier:
  - `tools/check_core3_checkout.py`
  - `tests/test_check_core3_checkout.py`
  - `docs/CORE3_BUILD_BASELINE.md`
- Protocol manifest validator rejects duplicate JSON keys, invalid UTF-8, non-standard JSON constants, oversized input, non-object roots, and malformed field types.
- Core3 checkout verifier checks the canonical upstream host/repository path, pinned commit, clean worktree, linked worktree layouts, and bounded Git command execution.
- Regression tests cover malformed manifest input, upstream URL acceptance/rejection, and checkout edge cases.
- CI workflow uses read-only repository permissions, concurrency cancellation, a five-minute job timeout, Python compile checks, manifest validation, and unit tests.
- Durable architecture and development notes are maintained in `docs/`.

## Core3 reconnaissance findings

Inspected upstream revision `403893d9b9f8e6fa712fbb3cb1fcd8f0fe45bb79`, including login, zone, session, packet dispatch, character selection, scene-ready, and movement source files.

- Login and zone services create datagram service threads and attach their respective handlers.
- Login and zone handlers associate sessions with network IDs; zone packet tasks can be ordered through the session task mechanism.
- Zone packet dispatch reads an operation count and 32-bit opcodes; unknown operations are logged/dropped.
- Object-controller messages have their own nested command dispatch and framing.
- Character selection validates ownership and account/session state, resolves the player, checks server/capacity conditions, binds the player to the zone session, restores saved location/containment, and marks the character online.
- Scene-ready callback operates on the player associated with the session.
- Movement serialization includes a message marker, object ID, signed 16-bit position components scaled by four, movement counter, and creature-specific speed/direction bytes. Coordinate conventions and validation still need deeper tracing.
- These findings are source reconnaissance only; they do not prove end-to-end runtime behavior.

Still unknown / requiring source tracing and eventual runtime verification:
- Transport encryption and credential protection.
- Reliability, sequencing, fragmentation, and compression behavior.
- Complete login/authentication and session handoff.
- Object create/destroy and baseline/delta replication.
- Full character spawn and movement acceptance/validation path.
- Persistence transaction boundaries and reconnect recovery.

## Current next steps

1. At the start of every continuation, inspect the live branch head, PR head/state, and exact-SHA CI. If the live head differs from this checkpoint, update the working base; never overwrite concurrent work.
2. Obtain a clean Linux environment or remote workstation and check out Core3 separately at the pinned commit.
3. Record actual toolchain/dependency versions and attempt the upstream debug build. Do not modify Core3 until a reproducible blocker is identified.
4. Continue the source audit: transport security, reliability/sequencing, fragmentation/compression, replication lifecycle, persistence transactions, reconnect, and movement validation.
5. Convert confirmed findings into concise, source-referenced audit documentation and targeted tests where possible.
6. Only after the audit and build baseline, select a narrow login-to-world-entry adapter proof of concept with explicit contract tests.
7. Unreal Engine client work remains a later milestone; this repository currently has no playable UE client, gateway implementation, or integrated Core3 checkout.

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
