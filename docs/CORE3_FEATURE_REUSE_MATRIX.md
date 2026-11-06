# Core3 Feature Reuse Matrix

**Source snapshot:** `swgemu/Core3` revision `403893d9b9f8e6fa712fbb3cb1fcd8f0fe45bb79`.

This is a source-level inventory. Detailed source paths, API names, GalaxyMMO dispositions, and verification gaps are recorded in [CORE3_REUSE_INVENTORY.md](CORE3_REUSE_INVENTORY.md). No row is yet certified **verified reusable** because GalaxyMMO has not built or executed this upstream revision.

| Capability | Source-level disposition | Primary Core3 subsystem | GalaxyMMO policy / remaining gate |
|---|---|---|---|
| Zone/server orchestration | Reuse candidate | ZoneServerImplementation and manager lifecycle | Preserve existing lifecycle; verify startup/shutdown and runtime health |
| Object creation/persistence | Reuse candidate | ObjectManager | Reuse object identity and persistence; verify transactions/recovery |
| World objects/containment | Reuse candidate | SceneObject, TangibleObject | Reuse transfer, slots, containers, zone placement; verify locks/permissions |
| Character lifecycle | Reuse candidate | PlayerManager, PlayerObject | Reuse creation/progression/online state; audit full account lifecycle |
| Sessions/task ordering | Reuse candidate | ZoneClientSession, ZonePacketHandler, ordered tasks | Preserve Core3 session ownership and ordering; verify teardown/reconnect |
| Entity state | Reuse candidate | CreatureObject, PlayerObject | Reuse authoritative state; verify mutation and replication semantics |
| Combat | Reuse candidate | CombatManager | Reuse resolver; verify damage, cooldown, range, LOS, PvP and exploit controls |
| Crafting | Reuse candidate | CraftingManager, schematic models | Reuse pipeline; verify recipe data, experimentation, persistence |
| Resources | Reuse candidate | ResourceManager, ResourceSpawner | Reuse spawn/survey/harvest; verify transaction atomicity and depletion |
| Loot | Reuse candidate | LootManager, ObjectManager | Reuse; verify ownership, randomization and persistence |
| Chat/mail | Reuse candidate | ChatManager, ChatRoom, PersistentMessage | Reuse; verify moderation, permissions, retention and rate limits |
| Groups/guilds | Reuse candidate | GroupManager, GuildManager, CreatureObject | Reuse; verify complete membership lifecycle and persistence |
| Missions/quests | Reuse candidate | MissionManager, PlayerObject quest journal | Reuse; verify objectives, rewards, timers and cleanup |
| Auction/vendor | Reuse candidate | AuctionManager, AuctionItem | Reuse; verify atomic currency/item transfer and concurrent purchase safety |
| Space/ships | Reuse candidate | SpaceZone, ShipManager and ship objects | Reuse candidate; verify movement, boarding, AI and replication |
| Spatial indexing | Reuse candidate | Octree/quadtree, close-object structures | Reuse spatial infrastructure; separately verify interest management |
| General entity replication | Unverified | BaseLineMessage, DeltaMessage, SceneObject send/broadcast APIs | Trace baselines/deltas, create/destroy, ordering and bandwidth |
| Movement acceptance/correction | Unverified | UpdateTransform and movement callbacks | Trace validation, counters, units, anti-cheat and reconciliation |
| Authentication/security | Reuse candidate, security gate open | LoginServer, account/session handlers | No direct client compatibility assumption; audit credential protection and session handoff |
| Database transaction guarantees | Unverified | ObjectManager, ObjectDatabase, ServerDatabase | Verify isolation, commit boundaries, crash consistency and recovery |

## Status vocabulary

- **Reuse candidate:** the subsystem and relevant API are present in the inspected source, but GalaxyMMO has not completed behavioral/build verification.
- **Unverified:** source-level review is incomplete or the specific guarantee has not been established.
- **Verified reusable:** only after a clean build and repeatable tests demonstrate the required behavior.
- **Needs extension:** existing behavior is sound but a specific requirement is missing.
- **Core patch required:** only after proving no supported configuration, data, Lua/script, or adapter extension can satisfy the requirement.

## Key architectural clarification

Core3 does not expose one standalone inventory manager in the inspected source. Inventory behavior is distributed across SceneObject containment/slot APIs, PlayerManager inventory/trade methods, and ObjectManager recursive persistence. GalaxyMMO should preserve this ownership model rather than create a parallel inventory database.

## Review record

See [CORE3_REUSE_INVENTORY.md](CORE3_REUSE_INVENTORY.md) for exact source paths and API names. Update this matrix with source revision, test evidence, and known limitations as each subsystem is audited.


## Economy integrity audit status

The deeper trace is in [CORE3_INVENTORY_TRADE_PERSISTENCE_AUDIT.md](CORE3_INVENTORY_TRADE_PERSISTENCE_AUDIT.md). Core3 has useful containment, permission, trade-validation, auction, and persistence primitives, but source review exposes unverified partial-commit windows. TransactionLog is audit logging, not an atomic transaction manager. Keep inventory/trade/auction as reuse candidates, not verified-safe, until concurrency, failure-injection, and restart tests pass.
