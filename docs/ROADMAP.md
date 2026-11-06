# Development Roadmap

The roadmap is milestone-based. A milestone is complete only when its acceptance criteria are demonstrated, not merely when files exist.

## M0 — Repository foundation

- [x] Establish project README and repository conventions.
- [x] Document system boundaries and server-authoritative rules.
- [x] Add a versioned protocol manifest and automated validation.
- [x] Add CI validation and unit tests.
- [x] Open a draft pull request for the foundation changes.

## M1 — Core3 technical reconnaissance

- [x] Inspect login and zone session/packet-dispatch entry points at a pinned source snapshot.
- [x] Record initial opcode/callback dispatch and object-controller framing.
- [x] Trace source-level character selection checks and scene-ready acknowledgement.
- [x] Record movement-transform field layout and coordinate ordering.
- [ ] Verify exact license file and notices at the pinned upstream revision.
- [ ] Build upstream in a clean supported Linux environment.
- [ ] Trace credential protection, transport reliability, sequencing, and session handoff end-to-end.
- [ ] Trace object creation, baseline/delta replication, containment, and movement validation end-to-end.
- [ ] Document runtime data prerequisites and legal constraints.
- [ ] Decide whether to use a gateway, adapter, selective reuse, or a separate server.

## M2 — Protocol and vertical-slice design

- [ ] Define authentication/session contract and version negotiation.
- [ ] Define character select/create contract.
- [ ] Define authoritative movement and entity replication contract.
- [ ] Define error model, idempotency, limits, and reconnect behavior.
- [ ] Build a protocol conformance test harness.

## M3 — Unreal client foundation

- [ ] Create the Unreal C++ project on a supported desktop workstation.
- [ ] Establish module boundaries, configuration, logging, and automated build.
- [ ] Implement connection lifecycle and protocol client against test server.
- [ ] Add basic login and character-selection UI using placeholder original assets.

## M4 — First playable vertical slice

- [ ] Spawn into one small original test zone.
- [ ] Replicate player movement and nearby entities.
- [ ] Support one interaction and one server-authoritative inventory operation.
- [ ] Persist character state and recover after reconnect.
- [ ] Measure latency, server tick cost, and client frame performance.

## M5 — Expand sandbox systems

Profession progression, gathering, crafting, resource variation, combat, creatures, missions, economy, player housing, social systems, and world tools are sequenced after the vertical slice validates the architecture.

## M6 — Production readiness

Security review, load testing, observability, backups, disaster recovery, moderation tools, deployment automation, accessibility, and operational runbooks.
