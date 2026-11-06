# GalaxyMMO Session Handoff

Use this file as the canonical restart point when continuing work in a new ChatGPT conversation.

## Current repository state

- Repository: https://github.com/ViViD420/GalaxyMMO
- Active branch: `development/foundation-hardening`
- Base branch: `main`
- Pull request: https://github.com/ViViD420/GalaxyMMO/pull/1
- PR state at last check: open, Draft; do not merge without the owner's approval.
- Last committed HEAD at this handoff: `3e6d3016bde7ff12458a8188d25029e1894aa569`
- Upstream Core3 source pin audited: `403893d9b9f8e6fa712fbb3cb1fcd8f0fe45bb79`
- Core3 build status: not yet built by GalaxyMMO.
- Latest CI for the last two earlier commits passed; CI for the handoff commit must be checked by exact SHA before claiming success.

## Project direction

GalaxyMMO is an original open-world sandbox MMORPG using Unreal Engine 5 + C++ for its planned client and SWGEmu Core3 as the intended server foundation. Preserve Core3's existing working systems wherever possible. Prefer configuration, data, Lua, and supported extension points. Make only the smallest necessary Core3 changes. Keep GalaxyMMO client-facing contracts separate from Core3 internals until an adapter strategy is proven.

Do not merge the PR, rewrite Core3 subsystems, claim a build passed without evidence, or include proprietary client binaries/assets/data.

## Work completed

- Foundation documentation, architecture decisions, protocol manifest, validator, tests, and CI workflow.
- Core3 login/zone/session/character/scene-ready/movement source reconnaissance at the pinned source revision.
- ADR-0003 documenting the Core3 preservation strategy.
- Core3 integration plan and feature reuse matrix.
- Draft authentication/session contract; no auth service or wire protocol has been implemented.
- Pinned Core3 build baseline and a read-only checkout verifier:
  - `tools/check_core3_checkout.py`
  - `tests/test_check_core3_checkout.py`
  - `docs/CORE3_BUILD_BASELINE.md`
- Updated README and development environment guide.

## Current next steps

1. Check PR head and CI results for the exact latest commit SHA.
2. Review and harden the new Core3 checkout verifier/tests if CI exposes issues.
3. Complete a clean checkout of the pinned upstream Core3 revision in a suitable Linux environment.
4. Record toolchain versions and attempt the upstream debug build; do not modify Core3 until a real blocker is reproduced.
5. Continue source audit of transport security, reliability/sequencing, object replication, persistence transactions, and reconnect lifecycle.
6. Only then select and implement the smallest viable client adapter vertical slice.

## Quick validation commands

From the GalaxyMMO repository root:

```sh
python tools/validate_protocol.py
python -m unittest discover -s tests -v
python tools/check_core3_checkout.py ../Core3
```

The third command requires a separate Core3 checkout at the audited commit.

## Restart instruction

When the user says:

> **Resume GalaxyMMO from the handoff checkpoint.**

First read this file and inspect the live GitHub branch, PR, and CI state. Use the live repository as source of truth if it has advanced beyond the SHA recorded above. Continue from the next unfinished step, commit all completed work to `development/foundation-hardening`, and report the exact commit SHA and actual CI status. Never overwrite concurrent changes or merge without explicit approval.
