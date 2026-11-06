# GalaxyMMO Session Handoff

Use this file as the canonical restart point when continuing work in a new ChatGPT conversation. The live branch is authoritative; this file is a checkpoint, not a substitute for checking GitHub.

## Current repository state

- Repository: https://github.com/ViViD420/GalaxyMMO
- Active branch: development/foundation-hardening
- Base branch: main
- Pull request: https://github.com/ViViD420/GalaxyMMO/pull/1
- PR state at checkpoint: open, Draft, not merged. Do not merge without explicit owner approval.
- Completed economy-audit content commit: 0e2d1c387198bff33836fcc3332b4f010655c566 (docs: audit Core3 economy transaction paths).
- This follow-up commit refreshes the handoff after the audit commit; always fetch live branch/PR head before continuing.
- Upstream Core3 source pin: 403893d9b9f8e6fa712fbb3cb1fcd8f0fe45bb79
- Core3 build status: not yet built by GalaxyMMO.
- Existing CI validates repository Python tooling and metadata; it does not build Core3 or Unreal.

## Project direction

GalaxyMMO is an original open-world sandbox MMORPG using Unreal Engine 5 + C++ for its planned client and SWGEmu Core3 as the intended server foundation. Preserve Core3's existing systems wherever they meet requirements. Prefer configuration, data, Lua, and supported extension points. Keep GalaxyMMO client-facing contracts separate from Core3 internals.

- Do not assume the UE5 client can speak the Core3 protocol directly.
- Do not duplicate Core3 account, character, inventory, persistence, or world-simulation systems without proving a need.
- Keep game state and economy server-authoritative.
- Do not merge the PR, patch upstream Core3, or claim a build/runtime test passed without evidence.
- The user currently works from an Android phone; no Core3 or Unreal build has been completed in this environment.
- Do not include proprietary client binaries, extracted assets, archives, art, audio, or data.
- Verify exact upstream licensing before copying/modifying/distributing Core3 source.

## Work completed

- Repository foundation, architecture/ADRs, protocol manifest/validator/tests/CI, Core3 reconnaissance, and reuse inventory.
- Inventory/trade/persistence source-audit milestone: added docs/CORE3_INVENTORY_TRADE_PERSISTENCE_AUDIT.md; updated the reuse inventory, feature matrix, and this handoff. Audit content is committed at 0e2d1c387198bff33836fcc3332b4f010655c566.
- Audit traces ContainerComponent transfer ordering; PlayerManager trade offer, validation, and finalization; AuctionManager listing, purchase, bid/refund, retrieval, startup reconstruction, cancellation, expiry, and deletion; ObjectManager dirty-object collection; Engine3 Berkeley DB child/master transactions; commit/checkpoint/shutdown; MySQL wrapper semantics; and TransactionLog.
- Critical finding: TransactionLog is audit logging, not a DB transaction or rollback system.
- Critical source-level trade risk: finalization does not roll back prior successful item transfers when a later transfer fails, and the shown method still proceeds to currency settlement.
- Critical source-level auction risk: instant-buy has a seller-null branch after buyer debit and SOLD status, then commits the audit log and returns without visible seller payout in that branch. Reachability/fallback requires runtime verification.
- Container move risk: old parent removal occurs before destination insertion; transfer does not itself invoke canAddObject.
- Persistence detail: Core3 pins Engine3 submodule 4cbf39336e0e727dfef861fbe65bd303ce70fd37. Dirty writes/deletes are staged in worker child transactions under a Berkeley DB master transaction; master uses commitSync then checkpoint. Mutation API is asynchronous relative to save pass.
- New high-confidence Engine3 risk: DatabaseManager::commitLocalTransaction uses the final write return code, so a non-deadlock error can be masked by a later successful write in the same child batch.
- New high-confidence Engine3 risk: CommitMasterTransactionThread ignores DatabaseManager::commitTransaction return value; worker serialization cleared dirty flags before master result is handled.
- Auction lifecycle: startup rebuilds AuctionsMap from persistent AuctionItem records; weak-reference expiry tasks and periodic maintenance overlap. Cancellation refund is asynchronous and bidder-online dependent in shown path; offline bidder expiry/cancellation and cancel-vs-expire races require tests.
- These are source findings, not reproduced exploits, runtime test results, or certification of current upstream head.
- GalaxyMMO has not changed Core3 source and has not implemented an economy transaction coordinator.

## Core3 audit provenance

- Upstream: https://github.com/swgemu/Core3
- Exact source revision: 403893d9b9f8e6fa712fbb3cb1fcd8f0fe45bb79
- Detailed audit: docs/CORE3_INVENTORY_TRADE_PERSISTENCE_AUDIT.md
- Reuse inventory: docs/CORE3_REUSE_INVENTORY.md
- Source pin may not be latest upstream; recheck before future source-dependent work.

## Next steps

1. Fetch live branch/PR head and exact-SHA CI before every continuation; never overwrite concurrent work.
2. Trace object-database manager/worker code beyond ObjectManager: serialization, write scheduling, STM/transaction boundaries, commit, checkpoint, tombstones, and recovery.
3. Complete auction expiration/cancellation callback paths and idempotency/restart semantics.
4. Obtain a clean supported Linux Core3 checkout at the pinned revision and reproduce failure-injection scenarios.
5. Only after evidence, design the smallest transaction coordinator or upstream extension needed for all-or-nothing inventory/economy operations.
6. Build a disposable-server vertical slice after build, transport, auth, replication, and persistence gates are met.
7. Unreal client work remains a later milestone; this repository does not yet contain a playable UE client or integrated Core3 runtime.

## Quick validation commands

From the GalaxyMMO repository root:

```sh
python -m compileall -q tools tests
python tools/validate_protocol.py
python -m unittest discover -s tests -v
python tools/check_core3_checkout.py ../Core3
```

The Core3 checkout checker requires a separate, clean Core3 checkout at the audited pin. Passing repository Python checks does not establish that Core3 or Unreal builds.

## Restart instruction

When the user says:

> Resume GalaxyMMO from the handoff checkpoint.

First read this file and inspect the live GitHub branch, PR, and CI state. Use the live repository as source of truth if it has advanced beyond the SHA recorded above. Continue from the next unfinished step, commit completed work to development/foundation-hardening, and report the exact commit SHA and actual CI status. Never overwrite concurrent work or merge without explicit approval.


## Latest deep audit checkpoint

- Audit source pins: Core3 `403893d9b9f8e6fa712fbb3cb1fcd8f0fe45bb79`; Engine3 `4cbf39336e0e727dfef861fbe65bd303ce70fd37`.
- Audit sections 8-10 trace Berkeley DB worker/master commit flow, error handling, checkpoint/shutdown, auction startup reconstruction, expiry, cancellation, refunds, and regression gates.
- Source inspection only: no clean Linux build, deterministic fault injection, crash/restart test, or runtime economy test has been executed. Do not claim complete economy functionality or patch upstream without reproducing the failure.
- Audit extension content commit: `01021180a56e9659bbee7966604faa9cf7a44eb8` (`docs: trace Berkeley DB commits and auction recovery`).


## Exact current repository checkpoint

- Branch head after handoff refresh: `3f45920172451853953fbff3142ba099c44f1280` (`docs: checkpoint Berkeley DB audit findings`).
- Tree: `2dc1232be479765f6835a53236a18bfb94683c50`.
- Push workflow run `42235370368`: success.
- PR workflow run `42235383427`: in progress at the time of this checkpoint; recheck exact-SHA CI before reporting completion.
- PR #1 remains open and Draft. Do not merge without explicit approval.


## CI follow-through

The exact branch head recorded above passed both repository validation workflows. This CI covers the GalaxyMMO repository's existing validation workflow; it does not compile Core3, Engine3, or Unreal Engine and does not run the proposed economy fault-injection scenarios.
