# Core3 Reuse Inventory for GalaxyMMO

## Scope and evidence standard

- Upstream: `https://github.com/swgemu/Core3`
- Inspected revision: `403893d9b9f8e6fa712fbb3cb1fcd8f0fe45bb79`
- GalaxyMMO branch: `development/foundation-hardening`
- This is a source-level inventory, not a build, runtime, security, or performance certification.
- A listed method is an available Core3 API/declaration at this revision. Native declarations identify implementation entry points, but do not by themselves prove all edge cases or production suitability.
- The source uses SWGEmu/Core3 terminology and data models. GalaxyMMO should expose its own stable DTOs/contracts to Unreal, not Core3 IDL/C++ types or legacy packet layouts.

## Executive decision

**Preserve Core3 as the authoritative owner of world/game state wherever its existing systems meet GalaxyMMO requirements.** Build only a thin GalaxyMMO-owned boundary for client identity, protocol translation, versioning, and any original game features that Core3 does not provide.

The strongest source-level reuse candidates are:
1. World objects, containment, spatial placement, object lifecycle, and persistence hooks.
2. Player/character lifecycle, progression, player state, and online-session handling.
3. Zone/session processing and ordered per-object task execution.
4. Combat resolution and combat state.
5. Crafting, schematics, experimentation, and resource spawning/harvesting.
6. Chat, groups, guilds, missions, auction/vendor systems, and ships/space systems.
7. Database access and object persistence infrastructure.

None should be labeled **verified reusable** until the pinned upstream code builds and a repeatable integration test demonstrates the required behavior.

## Reuse inventory

| System | Existing Core3 evidence at pinned revision | GalaxyMMO disposition | What remains to verify |
|---|---|---|---|
| Zone/server orchestration | `server/zone/ZoneServerImplementation.cpp` initializes ObjectManager, PlayerManager, ChatManager, CraftingManager, LootManager, ResourceManager, AuctionManager, MissionManager, GuildManager, ShipManager and zone managers. | **Reuse unchanged initially.** Do not create a second world-service lifecycle. | Startup/shutdown ordering, manager dependencies, failure recovery, multi-zone behavior, and build/runtime health. |
| Object creation and persistence | `server/zone/managers/object/ObjectManager.h`: `createObject`, `cloneObject`, `persistObject`, `persistSceneObjectsRecursively`, `loadPersistentObject`, `updatePersistentObject`, `destroyObjectFromDatabase`, `onCommitData`. | **Reuse unchanged initially.** Keep object identity and persistence authoritative in Core3. | Transaction boundaries, crash consistency, save scheduling, object-ID allocation, deletion semantics, and database recovery. |
| World objects and containment | `server/zone/objects/scene/SceneObject.idl`: `transferObject`, `removeObject`, `canAddObject`, `destroyObjectFromWorld`, `sendTo`, `sendDestroyTo`, `sendContainerObjectsTo`, `sendSlottedObjectsTo`, `getWorldPosition`, `switchZone`, `teleport`, `updateZone`, `broadcastObject`, `broadcastDestroy`. | **Reuse unchanged initially; adapt at boundary.** This is the foundation for world entities, containers, equipment slots, and spatial movement. | Locking/preconditions, containment rules, visibility recipients, zone transfer edge cases, client notification ordering, and persistence coupling. |
| Player/character lifecycle | `server/zone/managers/player/PlayerManager.idl`: `createPlayer`, `checkPlayerName`, `setFirstName`, `setLastName`, `awardExperience`, `calculatePlayerLevel`, `killPlayer`, `lootAll`, trade handlers, and structure ownership queries. | **Reuse lifecycle and progression.** Extend with data/config where possible; do not create a parallel character authority. | Full account-to-character path, ownership checks, name policy, simultaneous logins, creation/deletion, error handling, and persistence. |
| Player state and character features | `server/zone/objects/player/PlayerObject.idl`: account initialization, scene-ready, experience, waypoints, abilities, schematics, friends/ignore, faction standing, quest journal, online/offline/link-dead, reload and disconnect methods. | **Reuse unchanged where behavior matches; adapt client projection.** | Save semantics, reconnect races, state transition rules, and which methods are safe for external invocation. |
| Creature/entity state | `server/zone/objects/creature/CreatureObject.idl` derives from TangibleObject and contains player/creature state such as group/guild references, target, posture, wounds, skills, buffs, cooldowns, and movement-related values. | **Reuse Core3 entity model.** Do not mirror authoritative stats in a GalaxyMMO service. | Exact mutation APIs, AI/player distinction, state replication, movement validation, and concurrency. |
| Session task ordering | `server/zone/ZoneClientSession.idl`, `server/zone/ZonePacketHandler.cpp`, and `SceneObject.idl` ordered-task APIs. Existing zone packet processing queues tasks through session ordering; SceneObject also exposes pending/ordered task execution. | **Reuse internal scheduling.** Gateway must not bypass Core3 session/task ownership. | Ordering guarantees, queue bounds, cancellation, session teardown, duplicate/replay behavior, and concurrency tests. |
| Combat | `server/zone/managers/combat/CombatManager.h`: `startCombat`, `attemptPeace`, `forcePeace`, `doCombatAction` overloads, area target selection, duel operations, attack-speed and hit-chance calculations, combat broadcasts. | **Reuse combat authority; configure/tune first.** New combat rules should be narrow extensions rather than a second resolver. | Damage/mitigation pipeline, cooldowns, range/LOS, faction/PvP policy, exploit validation, persistence, and deterministic tests. |
| Crafting | `server/zone/managers/crafting/CraftingManager.idl`: schematic lookup, schematic groups, draft slots, resource weights, assembly success, experimentation success/failure, experiment rows, initial crafting values, serial generation. | **Reuse crafting pipeline and data models.** Prefer project-owned schematic/config data and supported extension points. | Recipe data loading, randomization, skill influence, resource constraints, item persistence, and exploit resistance. |
| Resource gathering | `server/zone/managers/resource/ResourceManager.idl`: resource spawning/shifting, survey list/results, sample messages, harvesting, resource-to-player transaction method, power accounting, current spawn lookup, recycling. | **Reuse resource lifecycle and harvesting.** | Spawn persistence/rotation, harvest transaction atomicity, tool/range checks, depletion rules, and economy balance. |
| Loot | `server/zone/ZoneServerImplementation.cpp` constructs and initializes `LootManager` with CraftingManager/ObjectManager. | **Reuse candidate.** Keep item creation and world-object persistence on Core3 side. | Loot table loading, random rolls, ownership/rights, duplicate handling, and persistence. |
| Chat and mail | `server/chat/ChatManager.idl`: player registration, room creation/destruction, persistent rooms, room lookup, group/guild/galaxy rooms, spatial chat configuration, persistent messages and mail-related types. | **Reuse chat/social backend; adapt message DTOs and moderation policy.** | Permission checks, mute/ignore enforcement, delivery semantics, message retention, rate limits, and spam controls. |
| Groups and guilds | Manager directories include group/guild managers; `CreatureObject.idl` stores group/guild references; `GuildManager.idl` includes guild loading, update/election, member/admin information, and chat integration. | **Reuse social state and membership lifecycle.** | Full group manager API, invite/leave/leader transitions, guild permissions, persistence, and reconnect behavior. |
| Missions and quests | `server/zone/managers/mission/MissionManager.idl`: mission list/accept/fail/abort/remove, mission generation/objectives, bounty list operations, NPC spawn allocation/free/despawn. PlayerObject includes quest journal/task methods. | **Reuse mission framework and quest state.** | Objective completion authority, mission persistence, timers, rewards, NPC cleanup, and project-specific mission types. |
| Auction/vendor economy | `server/zone/managers/auction/AuctionManager.idl`: add/check sale, create vendor item, query data, retrieve, buy, bid, instant buy, cancel, auction/vendor maintenance and expiration. | **Reuse market workflow.** Extend tax/fee/price policies via configuration where possible. | Currency/item atomicity, concurrent purchase races, listing ownership, expiration, offline delivery, and anti-dupe tests. |
| Database access | `server/db/ServerDatabase.h` exposes configured database selection and schema version; `server/zone/managers/object/ObjectManager.h` exposes object persistence operations. | **Reuse Core3 database/object persistence.** Do not write competing copies of Core3-owned records. | Database topology, schema migration process, transaction isolation, backup/restore, and failure behavior. |
| Space and ships | `ZoneServerImplementation.cpp` initializes ship managers and starts space zones; zone manager/object trees include ship, space, space-combat, and ship object systems. | **Reuse candidate for space zones and ship state.** | Full ship lifecycle, movement/physics authority, boarding, replication, AI, and client integration. |
| Spatial indexing/visibility | Zone tree contains octree/quadtree and close-object structures; `SceneObject` has range queries and broadcast operations. `VisibilityManager` specifically documents Jedi/bounty visibility, not general interest management. | **Reuse spatial world infrastructure; do not mistake the named VisibilityManager for general entity replication.** | Exact nearby-object selection, enter/leave range behavior, bandwidth, and baseline/delta replication. |
| Authentication/login | LoginServer/handlers and AccountVersion message are present; earlier audit confirms character selection validates the authenticated client's available characters before binding player to zone session. | **Reuse only after security and account lifecycle audit.** Keep GalaxyMMO identity/protocol boundary separate until proven. | Credential protection, password verification, rate limits, session token/handoff, account provider integration, and reconnect. |

## Important clarification: inventory is not a separate manager

The inspected tree does not establish a single standalone `InventoryManager` as the owner of all inventory behavior. Instead, inventory is represented through the Core3 scene-object/container/slot model and related player/trade APIs. The key extension points visible in the inspected declarations include:

- `SceneObject.transferObject`, `removeObject`, `canAddObject`, `getContainerObjects`, and `getSlottedObjects`.
- `SceneObject.sendContainerObjectsTo` and `sendSlottedObjectsTo`.
- `PlayerManager.getInventoryItemsOfType`, `getInsurableItems`, trade-window handlers, `checkTradeItems`, and `lootAll`.
- `ObjectManager.persistSceneObjectsRecursively` for recursive scene-object persistence.

Therefore, GalaxyMMO should reuse Core3's object containment, item ownership, equipment-slot, trade, and persistence behavior rather than inventing an independent inventory database. The complete inventory transaction and exploit-safety path still needs tracing.

## Integration boundary: what GalaxyMMO should own

GalaxyMMO-owned components should remain limited to concerns that Core3 cannot directly provide to the new UE5 client:

- Versioned client-facing protocol and stable DTOs.
- Authentication-provider integration, if Core3's current account model is not suitable after security review.
- Translation between UE client intent and approved Core3 operations.
- Client build/version negotiation and compatibility policy.
- Observability and gateway-level rate/size limits, without bypassing Core3 validation.
- Original GalaxyMMO-only features that have no suitable Core3 configuration/data/script extension.

Do not expose Core3 object IDs, packet structs, callback factories, IDL types, or internal C++ classes as public client contracts.

## Recommended reuse classification

| Classification | Systems |
|---|---|
| Reuse unchanged initially | Object manager/persistence; scene-object containment and lifecycle; zone orchestration; Core3 scheduling/task ownership |
| Reuse with GalaxyMMO boundary adaptation | Login/session; character entry; scene-ready; client object projection/replication; chat |
| Reuse and configure/tune | Combat; crafting; resources; loot; missions; auction/vendor; social systems; ships/space |
| Still unverified / do not design around yet | Full replication baselines/deltas and interest management; movement acceptance/correction; transport security/reliability; transaction guarantees; reconnect semantics |
| Core patch | None justified by this inventory. A patch requires a reproduced gap and proof that configuration, scripts/data, or an adapter cannot address it. |

## Next verification gates

1. Build the unmodified pinned Core3 revision in a clean supported Linux environment.
2. Trace and test the complete character entry path, including account/session handoff, spawn, baseline/delta messages, and scene-ready.
3. Trace object/container/inventory transfer and persistence transaction behavior, including simultaneous trade/buy/loot edge cases.
4. Trace movement acceptance, anti-cheat validation, and server correction.
5. Trace transport protection, reliability, sequencing, fragmentation, and compression.
6. Create a disposable-server vertical slice only after the above, proving login, character select, scene entry, one nearby entity, movement, disconnect, and reconnect.

## Source files inspected for this inventory

- `MMOCoreORB/src/server/zone/ZoneServerImplementation.cpp`
- `MMOCoreORB/src/server/zone/ZoneClientSession.idl`
- `MMOCoreORB/src/server/zone/ZonePacketHandler.cpp`
- `MMOCoreORB/src/server/zone/managers/object/ObjectManager.h`
- `MMOCoreORB/src/server/zone/managers/player/PlayerManager.idl`
- `MMOCoreORB/src/server/zone/managers/combat/CombatManager.h`
- `MMOCoreORB/src/server/zone/managers/crafting/CraftingManager.idl`
- `MMOCoreORB/src/server/zone/managers/resource/ResourceManager.idl`
- `MMOCoreORB/src/server/zone/managers/auction/AuctionManager.idl`
- `MMOCoreORB/src/server/zone/managers/mission/MissionManager.idl`
- `MMOCoreORB/src/server/zone/managers/guild/GuildManager.idl`
- `MMOCoreORB/src/server/chat/ChatManager.idl`
- `MMOCoreORB/src/server/zone/objects/scene/SceneObject.idl`
- `MMOCoreORB/src/server/zone/objects/creature/CreatureObject.idl`
- `MMOCoreORB/src/server/zone/objects/player/PlayerObject.idl`
- `MMOCoreORB/src/server/db/ServerDatabase.h`

