# GalaxyMMO Architecture

## Product direction

GalaxyMMO is an original science-fiction sandbox MMORPG. Its design takes inspiration from player-driven virtual worlds and profession-focused sandbox games, while using original setting, names, lore, art, audio, and game content.

## System boundaries

- **Unreal client:** presentation, input, local prediction where safe, UI, audio, and rendering. The client is never authoritative for currency, inventory ownership, combat outcomes, progression, or persistence.
- **Game services:** authentication/session orchestration, world simulation, character state, inventory, economy, combat, crafting, social systems, and persistence.
- **Core3 evaluation:** SWGEmu Core3 is a candidate server foundation, not an assumed drop-in backend. Its original client protocol and runtime assumptions must be audited before integration is selected.
- **Integration layer:** explicit protocol contracts and adapters isolate the Unreal client from Core3 internals. No client-facing contract should expose Core3 implementation types.
- **Data layer:** durable state changes are transactional where practical; migrations are versioned and repeatable.

## Authority and trust

The server validates every consequential command. A client submits intent (for example, request to equip an item); the server checks identity, permissions, range, item ownership, capacity, cooldowns, and game rules before committing a result. Clients may render predicted feedback, but must reconcile to server-confirmed state.

Never trust client-supplied prices, damage, item stats, positions for restricted interactions, permissions, or progression values. Validate message size, schema version, rate, and session ownership at the boundary.

## Reliability requirements

- Commands that may be retried need idempotency keys or explicit duplicate handling.
- Persist critical state before acknowledging success.
- Use bounded queues and timeouts; do not allow unbounded per-session memory growth.
- Log structured event context without credentials, tokens, or unnecessary personal data.
- Make protocol and database changes versioned and documented.

## Proposed repository layout

```text
Client/                 Unreal Engine client (added when desktop toolchain exists)
Database/               migrations and data contracts
Integration/Protocol/    client/server protocol contracts
Server/                  Core3 evaluation and GalaxyMMO-owned services
Tools/                   validation and developer utilities
docs/                    architecture, decisions, setup, and milestones
.github/workflows/       automated validation
```

## Architecture decision process

Material choices belong in `docs/decisions/` as short Architecture Decision Records (ADRs): context, decision, alternatives, consequences, and revisit conditions. Do not commit to direct Core3 protocol compatibility until source-level reconnaissance and a proof of concept demonstrate it.
