# Core3 Inventory, Trade, and Persistence Transaction Audit

## Scope and evidence

- Upstream: https://github.com/swgemu/Core3
- Exact inspected revision: 403893d9b9f8e6fa712fbb3cb1fcd8f0fe45bb79
- Source-level trace only. No Core3 build, live server, concurrency test, crash test, or exploit reproduction has been performed.
- No Core3 source code is copied into GalaxyMMO.
- TransactionLog is an audit/logging facility. Its commit method does not itself commit a database transaction or roll back game-state mutations.

## Executive assessment

Core3 provides the correct foundation to reuse: a scene-object graph, parent/child containment, equipment slots, container permissions, player trade logic, auction workflows, and object persistence hooks. GalaxyMMO should not create a parallel inventory database or second item-ownership authority.

The source trace nevertheless identifies high-priority economy-integrity risks:

1. Container transfer removes the old parent before destination insertion succeeds. The transfer implementation does not itself call canAddObject.
2. Player trade can partially apply item transfers. It does not roll back earlier successful moves when a later move fails, and the shown finalization continues to currency settlement.
3. Auction operations span in-memory maps, persistent listing records, scene-object movement, currency mutations, taxes, and mail. The inspected methods do not demonstrate one atomic database transaction spanning those effects.
4. ObjectManager::updatePersistentObject only marks an object updated. It is not a synchronous durable commit.
5. TransactionLog::commit finalizes an audit record, not an economy transaction.

These are source-level risks, not reproduced live exploits. Keep all affected systems as reuse candidates, not verified-safe, until fault-injection and restart tests pass.

## 1. Inventory and containment

### Source path

- MMOCoreORB/src/server/zone/objects/scene/SceneObjectImplementation.cpp
- MMOCoreORB/src/server/zone/objects/scene/components/ContainerComponent.cpp
- MMOCoreORB/src/server/zone/objects/scene/SceneObject.idl

SceneObjectImplementation delegates canAddObject, transferObject, and removeObject to its configured ContainerComponent. The component checks self-containment, no-trade rules, container type, slot arrangement, volume limits, and parent/ownership relationships. Container permissions are a separate check; a successful capacity/type check does not prove the actor has permission to move an item.

### Transfer sequence and risk

ContainerComponent::transferObject follows this broad sequence:

1. Reject self-transfer and objects that cannot be transferred.
2. Cancel an active slicing session on the item.
3. Read the old parent and zone.
4. Ask the old parent to remove the item, suppressing client notification.
5. Remove the item from its old zone if needed.
6. Lock the destination container.
7. Check slot occupancy or enforce volume capacity when allowOverflow is false.
8. Insert the item and set its new parent and containment type.
9. Release the destination lock, notify clients/observers, and mark the destination for database update.

The method does not internally call canAddObject. The destination volume check occurs after source removal. Thus a destination-capacity failure can happen after the old parent has already been asked to remove the object. The exact recovery behavior must be tested; do not assume a failed transfer restores the old parent. A separate canAddObject preflight is not a reservation and can become stale before transfer.

The inspected path locks the destination container after source removal; it does not demonstrate one lock spanning both source and destination containers. A race between two simultaneous moves of the same object is therefore a required test, not something to assume is safe because container locks exist.

checkContainerPermission separately resolves owner permissions, privileged access for selected permissions, inherited permissions, and group allow/deny masks. Every client-originated move must pass the correct permission check before invoking a transfer.

### Nested items

PlayerManager's trade offer handler accepts an item that is a sub-child of the player and checks MOVECONTAINER permission. Final trade validation separately checks the player's inventory/datapad with hasObjectInContainer. Verify the exact lookup semantics for nested descendants. Test direct inventory items and items nested several containers deep to ensure the offer UI and final server validation agree.

### Persistence coupling

A successful container transfer calls updateToDatabase on the destination container when its container map changed. This marks state for the object database update machinery; it does not prove that serialized state is durably committed before the operation returns. Test both sides of a move across process crash and database failure.

## 2. Player trade

### Source path

- MMOCoreORB/src/server/zone/managers/player/PlayerManagerImplementation.cpp
- MMOCoreORB/src/server/zone/objects/player/sessions/TradeSession.idl
- MMOCoreORB/src/server/zone/objects/transaction/TransactionLog.cpp

### Offer and validation

handleAddItemToTradeWindow requires an active trade session, a valid player target, an item that is a sub-child of the initiating player, MOVECONTAINER permission, and no no-trade flag or recursively contained no-trade item. It records the item in TradeSession and sends its presentation to the receiver.

handleGiveMoneyMessage clamps the offered amount to the player's current cash credits and stores it in session state. It does not escrow or debit the amount at offer time.

TradeSession stores target ID, a no-duplicate sorted item list, accepted/verified flags, and money amount. It is transient session state, not a durable transaction ledger.

checkTradeItems requires both player arguments to be locked. It verifies reciprocal targets and sessions; item tradeability; destination canAddObject; source inventory/datapad containment; pet, faction pet, droid, vehicle, and ship restrictions; capacity counts; nonnegative and affordable cash offers; and distance under 15 units.

This is useful server-side validation and should be reused. It does not reserve items, capacity, or currency. Final validation must run under a defined lock scope immediately before mutation.

The manual trade capacity comparisons use current size plus incoming count greater-than-or-equal-to volume limit. The generic container check rejects insertion when current size is already at the limit. The trade comparison may therefore reject filling the final free slot exactly. Test the boundary; it is likely a conservative capacity discrepancy rather than a duplication issue.

### Finalization and partial-commit risk

handleVerifyTradeMessage marks the initiating session verified, resolves and locks both players, re-fetches the receiver's session, and re-runs checkTradeItems. If the receiver session is also verified, it transfers items from the first player, transfers items in the reverse direction, exchanges cash credits, sends trade-complete messages, clears both sessions, and clears both target IDs.

The shown code has a serious partial-commit weakness:

- In the first item loop, the return value from objectController->transferObject is not used to abort or fail the trade.
- In the reverse loop, transfer failures are logged, but previously successful item transfers are not rolled back.
- The method proceeds to exchange currency after the item loops, regardless of item-transfer failures.
- No compensating move or durable two-party commit protocol is visible in this method.
- TradeSession has acceptedTrade and verifiedTrade flags. Accept/unaccept handlers set acceptedTrade, while the shown finalization gates on the other session's verifiedTrade. Trace the complete packet/callback sequence before interpreting the client UI state; test accept/unaccept/verify interleavings.

This creates a credible partial-trade failure mode: some items may move, another item may fail, and currency may still exchange. It has not been reproduced on a running server.

### Required trade invariants

- Every item has exactly one authoritative parent before and after trade.
- Both complete item sets and both currency amounts are validated before mutation.
- Trade either commits all item and currency changes or leaves both players unchanged.
- A failed transfer cannot silently proceed to currency settlement.
- Duplicate/reordered accept, verify, abort, and retry packets cannot apply the trade twice.
- Offer changes, item movement, cash spending, disconnect, timeout, or range violation invalidate prior acceptance/verification as required.
- Sessions are cleared on success, cancellation, timeout, disconnect, and participant invalidation.
- Restart at every commit boundary recovers to the complete pre-trade or complete post-trade state.

## 3. Auction and vendor economy

### Source paths

- MMOCoreORB/src/server/zone/managers/auction/AuctionManagerImplementation.cpp
- MMOCoreORB/src/server/zone/managers/auction/AuctionsMapImplementation.cpp
- MMOCoreORB/src/server/zone/objects/auction/AuctionItemImplementation.cpp

### Listing

The listing path validates price, vendor, ownership/move-out permission, vendor/commodity limits, item type, and other sale restrictions. It creates an AuctionItem record, persists it in the auctionitems object database, adds it to the in-memory AuctionsMap, and creates a TransactionLog with auto-commit disabled and related-object export enabled. On map-add failure it aborts the log and removes the commodity-limit entry. On success it destroys the original item from the world, commits the audit log, charges bazaar sale fees afterward, marks the auction record persistent, and schedules expiry.

AuctionsMap is an in-memory index protected by its own lock; AuctionItem is the persistent listing record. The source does not show a database transaction spanning listing creation, map insertion, original item world removal, fee debit, and expiry scheduling. Test crashes at each boundary, including cases where the listing record exists while the original item still exists, or vice versa.

### Instant purchase

buyItem resolves the listing/vendor, rejects missing or sold listings and self-purchases, checks bank credits and price, and calls doInstantBuy for non-auction listings.

doInstantBuy locks the listing, updates auction-owner indexing, marks the listing SOLD, sets buyer ID/name and expiry, creates a non-auto-committing TransactionLog, subtracts buyer bank credits, and sends notifications/mail. Seller credit is applied later under the seller creature lock, followed by TransactionLog::commit. City tax is a subsequent separate debit/treasury update.

A high-priority branch is explicit: if the seller creature lookup returns null, the code adds an error to the TransactionLog, commits the audit log, and returns after buyer debit and SOLD status, without visible seller payout in that branch. Whether an offline seller can produce this state and whether another payout mechanism exists must be tested. The audit-log commit does not restore the buyer's credits or reverse SOLD status.

Buyer debit, seller credit, tax debit, city treasury credit, mail delivery, and listing status are not shown inside one atomic database transaction. A crash or error between them can leave partially settled state.

### Bids, refunds, retrieval, deletion

Bid processing changes listing price/proxy/bidder fields and debits/refunds bank credits through separate object mutations and audit logs. Some outbid refunds are scheduled asynchronously. Test duplicate bid messages, concurrent bids, bidder disconnects, delayed refunds, and restart recovery.

Retrieval validates status, owner/buyer identity, distance/location, and destination capacity. It locks the listing and player, transfers the auctioned scene object to inventory/datapad, commits the audit log, broadcasts the object, marks the listing RETRIEVED, deletes the auction record through AuctionsMap, and clears its auctioned-object ID. Item transfer and listing deletion are sequential separate operations. Test crashes after transfer but before status update, after status update but before listing deletion, and during object deletion.

AuctionItemImplementation::destroyAuctionItemFromDatabase can mark the listing DELETED, clear its item ID, and schedule associated scene-object deletion on a task queue. Test asynchronous cleanup for idempotency under restart and duplicate requests.

## 4. Persistence and database boundaries

### Source paths

- MMOCoreORB/src/server/zone/managers/object/ObjectManager.cpp
- MMOCoreORB/src/server/db/ServerDatabase.cpp
- MMOCoreORB/src/server/db/MySqlDatabase.cpp
- MMOCoreORB/src/server/db/MySqlDatabase.h
- MMOCoreORB/src/odb/ObjectDatabaseCore.cpp

### ObjectManager

persistObject assigns an object-database ID when needed, sets persistence level, and calls updatePersistentObject. persistSceneObjectsRecursively walks child objects, slotted objects, and contained objects recursively. updatePersistentObject itself only calls _setUpdated(true) and returns. It does not synchronously serialize or commit the object. destroyObjectFromDatabase marks the loaded object for deletion; durable deletion is handled by the database lifecycle. loadPersistentObject resolves the database from the high bits of the object ID and deserializes the stored object.

Therefore, success at the ObjectManager API layer must not be interpreted as durable commit. Trace the object-database worker/commit/checkpoint lifecycle and acknowledgement ordering before deciding when a client may be told that an item move or purchase is final.

### Separate relational and object persistence

Persistent scene objects use the object-database layer and database IDs. ServerDatabase's MySQL layer separately manages relational records and schema metadata. ObjectManager::onCommitData copies dirty character-directory metadata from characters_dirty into characters using REPLACE and then deletes corresponding dirty rows. This is not the same operation as saving inventory object graphs.

MySqlDatabase exposes commit, rollback, and autocommit. Connection setup calls autocommit(false) only under WITH_STM; execution and commit behavior depend on build configuration. Do not infer that scene-object persistence participates in those MySQL transactions. Trace the object-database manager and STM configuration independently.

### TransactionLog is not a transaction manager

TransactionLog captures source/destination/subject IDs, metadata, before/after credit balances, state, and optional related-object exports. It can group related events and write/export the record. Its commit finalizes the audit record. It does not hold a database transaction open, snapshot and restore object state, reserve inventory capacity, undo mutations, or coordinate locks across participants.

## 5. Risk register

| Area | Finding | Severity before tests | Confidence |
|---|---|---:|---|
| Container move | Source removal precedes destination insertion; transfer does not internally call canAddObject | High | High: direct source order |
| Concurrent moves | Preflight and mutation are separate; no combined source/destination lock shown | High | High for inspected path; runtime race untested |
| Player trade | Partial item moves are not rolled back; first direction ignores failure; currency settlement continues | Critical | High: direct source flow |
| Trade state | accepted and verified flags have separate handlers; finalizer checks verified flag | Medium | High for shown methods; packet sequence unverified |
| Trade capacity | greater-than-or-equal comparison may reject final free slot | Low | Medium: boundary semantics need test |
| Auction listing | record, map, world removal, fee, and expiry are separate steps | High | High: direct source sequence |
| Instant purchase | seller-null branch commits audit log after buyer debit and SOLD state without visible seller payout | Critical | High for branch; reachability/fallback unverified |
| Auction settlement | buyer debit, seller credit, tax, treasury, and mail are separate mutations | High | High: direct source sequence |
| Retrieval/deletion | item transfer, listing status, map removal, and DB deletion are sequential | High | High: direct source sequence |
| Object durability | updatePersistentObject only marks dirty; durable commit timing unestablished | High | High: direct implementation |
| TransactionLog | audit record only; no rollback or DB atomicity | Critical misconception risk | High |
| Character directory | dirty-row copy uses REPLACE then DELETE in shown path | Medium | High: direct implementation; SQL config untested |

Severity is a pre-verification risk rating, not a statement that a live exploit has been reproduced.

## 6. Required verification plan

### Inventory and containment
1. Move direct and deeply nested items between inventory, bank, datapad, vendor, corpse, and world containers.
2. Test self-transfer, cycles, no-trade descendants, wrong permissions, occupied slots, incompatible container types, and full destinations.
3. Inject destination insertion failure after source removal; assert exactly one valid parent or successful restoration.
4. Race two moves of the same item to different destinations; assert one winner and no duplicate/lost item.
5. Crash after source removal, destination insertion, and before/after persistence acknowledgement; compare the recovered object graph.
6. Verify clients cannot observe success before durable state is accepted.

### Player trade
1. Test item-only, credit-only, mixed, datapad, pet/vehicle/ship, nested-container, and full-inventory-boundary trades.
2. Inject failure on the first item transfer and every later transfer; assert no item or credit changes survive a failed trade.
3. Send duplicate, reordered accept/unaccept/verify/abort packets; assert exactly one outcome.
4. Change offers, move offered items, spend offered credits, disconnect either participant, and leave range between accept and verify.
5. Run concurrent trades involving the same item/player; assert no duplicate ownership or negative balance.
6. Restart at every step; recover to exactly pre-trade or post-trade state.

### Auction/vendor
1. Race concurrent instant purchases; exactly one buyer may be charged and receive ownership.
2. Test seller online, offline, deleted, renamed, and unavailable; never debit a buyer without recoverable payout or refund.
3. Inject failures between status, buyer debit, seller payout, tax, treasury, and mail; assert deterministic recovery.
4. Race bid, cancel, expiry, and retrieve; assert one terminal state and one item owner.
5. Duplicate retrieval/deletion requests; assert idempotency.
6. Restart after listing creation, map insertion, original item removal, purchase, and retrieval.

### Persistence
1. Trace the complete object-database write path from _setUpdated through worker scheduling, serialization, commit, and checkpoint.
2. Force DB lock timeout, DB outage, disk-full, process kill, and restart during writes.
3. Verify object IDs, tombstones/deletion, recursive graph persistence, and parent/child recovery.
4. Test divergence and reconciliation between object graph and relational metadata.
5. Test each supported DB build/configuration separately, including WITH_STM if enabled.
6. Verify backups restore a consistent world/economy state.

## 7. GalaxyMMO integration decision

- Reuse Core3's scene-object graph, containment/slot model, permission model, PlayerManager trade rules, AuctionManager/AuctionItem workflows, and ObjectManager persistence as the baseline.
- Do not duplicate inventory ownership or create a parallel inventory database.
- Do not expose trade, purchase, retrieval, or inventory-move commands through a UE-facing gateway until each operation has an all-or-nothing contract and fault-injection evidence.
- Translate client intent into validated Core3 operations. Never accept client-supplied parent IDs, ownership, balances, auction status, or persistence flags as authoritative.
- No Core3 patch is justified by source review alone. Reproduce the failure in a supported build, check upstream fixes, and exhaust config/script/data/adapter options first.
- A future server-owned transaction coordinator may be needed if Core3 cannot guarantee all-or-nothing economy changes. It must orchestrate Core3-owned objects and persistence rather than become a second inventory authority.

## Source paths reviewed

All paths refer to the exact pinned Core3 revision.

- MMOCoreORB/src/server/zone/objects/scene/SceneObjectImplementation.cpp
- MMOCoreORB/src/server/zone/objects/scene/components/ContainerComponent.cpp
- MMOCoreORB/src/server/zone/managers/player/PlayerManagerImplementation.cpp
- MMOCoreORB/src/server/zone/objects/player/sessions/TradeSession.idl
- MMOCoreORB/src/server/zone/managers/auction/AuctionManagerImplementation.cpp
- MMOCoreORB/src/server/zone/managers/auction/AuctionsMapImplementation.cpp
- MMOCoreORB/src/server/zone/objects/auction/AuctionItemImplementation.cpp
- MMOCoreORB/src/server/zone/managers/object/ObjectManager.cpp
- MMOCoreORB/src/server/zone/objects/transaction/TransactionLog.cpp
- MMOCoreORB/src/server/db/ServerDatabase.cpp
- MMOCoreORB/src/server/db/MySqlDatabase.cpp
- MMOCoreORB/src/server/db/MySqlDatabase.h
- MMOCoreORB/src/odb/ObjectDatabaseCore.cpp

## Next source-audit gate

Trace the object-database manager/worker implementation, including STM boundaries, serialization, commit, checkpoint, deletion, and recovery. Then complete auction expiration/cancellation callback paths and implement reproducible fault-injection tests in a clean Linux checkout. Until those tests pass, the listed risks remain open.
