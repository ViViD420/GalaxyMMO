# ADR-0002: Keep the client/server boundary independent of Core3 internals

- **Status:** Accepted for initial development
- **Date:** 2026-11-06

## Context

The project plans a new Unreal Engine client while evaluating SWGEmu Core3 as a possible server foundation. Core3's README describes a server emulator for the classic game environment; compatibility with a new client must not be assumed.

## Decision

Define GalaxyMMO-owned client/server contracts in `Integration/Protocol/`. Keep Core3-specific code behind a server adapter until a source audit and integration proof of concept justify a more direct approach. The server remains authoritative for consequential game state.

## Alternatives considered

1. **Assume direct protocol compatibility:** rejected because no evidence currently establishes it.
2. **Fork and deeply modify Core3 immediately:** deferred because it creates maintenance and upgrade risk before the networking and gameplay boundaries are understood.
3. **Build an adapter boundary first:** selected because it allows independent client development and makes integration decisions reversible.

## Consequences

- Additional adapter work may be required.
- The client can evolve against a stable contract.
- Core3 can be evaluated incrementally without coupling all client code to its internal types.
- Transport and serialization remain undecided until measured requirements and source reconnaissance are available.
