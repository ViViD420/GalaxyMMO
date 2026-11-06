# Core3 Reconnaissance

## Snapshot inspected

- **Repository:** https://github.com/swgemu/Core3
- **Inspected source revision:** `403893d9b9f8e6fa712fbb3cb1fcd8f0fe45bb79`
- **Branch context:** upstream `unstable` source snapshot returned by GitHub code search
- **Build status:** not built by GalaxyMMO yet
- **License status:** upstream README identifies AGPL-3.0-or-later; verify the exact revision's LICENSE/COPYING files before incorporating code.

This is a source-level reconnaissance snapshot, not a claim that this commit is the latest upstream revision or that it compiles in our environment.

## Findings confirmed from source

### Login path

At the inspected revision:

- `MMOCoreORB/src/server/login/LoginServerImplementation.cpp` constructs a `DatagramServiceThread`, attaches a `LoginHandler`, creates a `BasePacketHandler`, and deploys a `LoginProcessServerImplementation`.
- The login handler maps connections by the session's network ID and delegates packets to `LoginServerImplementation::handleMessage`.
- The login implementation passes available sessions and packets to its base packet handler; processing messages creates a `LoginMessageProcessorTask`.

### Zone path

- `MMOCoreORB/src/server/zone/ZoneServerImplementation.cpp` constructs a `DatagramServiceThread` and attaches a `ZoneHandler` when starting.
- The zone handler maps `ZoneClientSession` objects by network ID and delegates incoming packets to the zone server.
- Zone packet processing calls `ZonePacketHandler::generateMessageTask`; accepted tasks are queued through the session's ordered-task mechanism when a session exists.
- `ZoneClientSession.idl` includes account ID, session ID, player reference, character and banned-character maps, pending tasks, command spam cooldown, and command count. It also exposes a `BaseClientProxy` session.
- `ZonePacketHandler.cpp` registers a large set of message callbacks by 32-bit opcode. Object-controller messages are dispatched through a second callback factory using 32-bit command identifiers.
- `generateMessageTask` parses a 16-bit operation count followed by a 32-bit opcode, creates a callback, parses its message, and returns a task/callback only when parsing succeeds. Unknown opcodes are logged and dropped.
- `ObjectControllerMessage.h` constructs a message with a 16-bit marker, a fixed 32-bit CRC, two 32-bit header values, a 64-bit object ID, and a 32-bit zero field; compression is configurable.

## Architectural implications

1. Core3's login and zone paths are built around its own datagram service, packet abstractions, session objects, callback factories, and object/task model.
2. The protocol is not a generic REST or WebSocket API. The opcode registry and object-controller framing are specific protocol machinery.
3. A new Unreal client should not be declared compatible based only on reusing the server. A gateway/adapter or a GalaxyMMO-owned protocol is still the safer working assumption.
4. Core3's session and task lifecycle may be useful to study, but exposing its internal types directly to a new client would tightly couple the client to the emulator.
5. The source review has not yet traced authentication cryptography, transport reliability, compression implementation, all packet encodings, or object replication end-to-end.

## Evidence paths

All paths below refer to the inspected SHA above:

- `MMOCoreORB/src/server/login/LoginHandler.h`
- `MMOCoreORB/src/server/login/LoginServerImplementation.cpp`
- `MMOCoreORB/src/server/zone/ZoneClientSession.idl`
- `MMOCoreORB/src/server/zone/ZoneHandler.h`
- `MMOCoreORB/src/server/zone/ZonePacketHandler.h`
- `MMOCoreORB/src/server/zone/ZonePacketHandler.cpp`
- `MMOCoreORB/src/server/zone/ZoneServerImplementation.cpp`
- `MMOCoreORB/src/server/zone/packets/object/ObjectControllerMessage.h`

## Remaining questions

- Trace the exact login message sequence, password/authentication handling, version checks, and token/session handoff.
- Inspect the transport implementation and determine whether "DatagramServiceThread" is the only transport path used for these flows; map reliability, sequencing, fragmentation, encryption, and compression.
- Trace a complete character selection, scene-ready, movement, and replication lifecycle.
- Locate object create/destroy and baseline/delta replication serializers.
- Identify where persistence transactions occur for character and inventory operations.
- Build the upstream server from a clean supported environment and record exact toolchain/results.
- Confirm license notices and runtime data prerequisites from the pinned revision.

## Current decision

Do not implement a direct Core3 wire-compatible Unreal client yet. Continue with a GalaxyMMO-owned protocol boundary and evaluate a gateway/adapter after the missing network and replication paths are understood.
