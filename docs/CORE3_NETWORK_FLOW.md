# Core3 Network Flow Notes

**Source snapshot:** `403893d9b9f8e6fa712fbb3cb1fcd8f0fe45bb79` of `swgemu/Core3`.

This document records only what the inspected source files demonstrate. It is not a complete protocol specification.

## Login connection and packet path

1. `LoginServerImplementation` creates a `DatagramServiceThread`.
2. It attaches a `LoginHandler` to that service.
3. It creates a `BasePacketHandler` and a `LoginProcessServerImplementation`.
4. On connection, it wraps the socket/address in `BaseClientProxy`, initializes the proxy against the datagram service, and creates a `LoginClient`.
5. `LoginHandler` stores the login client by network ID and routes packets to `LoginServerImplementation::handleMessage`.
6. The login server passes available sessions and packets to the base packet handler. Its process-message path creates a `LoginMessageProcessorTask`.

**Not yet established:** exact authentication exchange, password hashing/proof, encryption, sequencing, retransmission, and session handoff to the zone server.

## Zone connection and packet path

1. `ZoneServerImplementation` creates a `DatagramServiceThread` and starts it with a `ZoneHandler`.
2. On connection, the zone server creates and initializes a `BaseClientProxy`, then creates a `ZoneClientSession`.
3. `ZoneHandler` stores the session by network ID and forwards incoming packets to the zone server.
4. The zone server's base packet handler processes packets; queued messages are passed to `ZonePacketHandler::generateMessageTask`.
5. The zone packet handler parses a 16-bit operation count and 32-bit opcode, resolves a callback, and asks it to parse the remainder.
6. When a client session exists, the resulting task is queued through `executeOrderedTask`, which uses the session's pending-task mechanism.

## Dispatch layers

The inspected source shows two layers of dispatch:

- Outer message dispatch: 32-bit opcode to a registered message callback.
- Object-controller dispatch: after the outer object-controller message is recognized, a second factory maps a 32-bit command identifier to a specific callback.

This layered dispatch means a compatibility effort would need exact framing, byte order, compression behavior, opcode registry, command registry, and payload layouts—not just message names.

## GalaxyMMO design implications

- Keep client-visible message DTOs independent of Core3 C++ classes and IDL types.
- Version the GalaxyMMO protocol separately.
- Validate session ownership and command authorization on the server.
- Use bounded payload sizes, explicit timeouts, replay/idempotency handling, and structured error codes in the new contract.
- Do not copy Core3 packet layouts into GalaxyMMO until there is a deliberate compatibility requirement and a documented legal/technical review.
