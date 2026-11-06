# Core3 Authentication, Character Entry, and Replication Audit

## Scope and provenance

- Upstream: https://github.com/swgemu/Core3
- Inspected revision: `403893d9b9f8e6fa712fbb3cb1fcd8f0fe45bb79`
- This is a source review only. GalaxyMMO has not built or executed this upstream revision.
- Findings are limited to the listed source files; this is not a complete packet or security specification.

## Login message evidence

`MMOCoreORB/src/server/login/packets/AccountVersionMessage.h` constructs a message with:

1. a 16-bit value `0x04`;
2. a 32-bit value `0x41131F96`;
3. ASCII username;
4. ASCII password;
5. ASCII client version;
6. a 32-bit SWGEmu string hash.

Its parse method reads username, password, and version as ASCII strings. This establishes the message's field layout in this source snapshot; it does **not** establish whether credentials are protected by transport encryption, obfuscation, or another layer. That must be traced in the transport/proxy implementation before any security conclusion is made.

`LoginPacketHandler.h` declares handlers for client permissions, character selection, scene-ready, login client ID, and character deletion. This indicates the login service participates in more than a single username/password exchange, but handler declarations alone do not establish their full behavior.

## Character selection and session binding

`SelectCharacter.h` serializes a 16-bit marker, the hash of `SelectCharacter`, a 64-bit character ID, and the SWGEmu string hash.

`SelectCharacterCallback.h` demonstrates important server-side checks and lifecycle steps:

- The requested character ID is checked against the authenticated client's available characters for the active galaxy.
- The server resolves the character object and verifies it is a player creature.
- Server loading/shutdown state is checked.
- Server capacity, server lock state, and per-account online-character limits are checked during connection.
- The server binds the player object to the zone session.
- The player's saved zone and containment/parent state are considered when restoring the character.
- The player is marked online and related managers are notified after successful placement.

This is strong evidence for a server-authoritative character-entry flow. It also shows that re-entry is not simply “load object and spawn at XYZ”: containment, ships/cells, logout state, connection replacement, and online limits affect restoration.

## Scene-ready acknowledgement

`CmdSceneReady.h` defines a small message containing a 16-bit marker, a 32-bit identifier, and a parsed 16-bit acknowledgement sequence.

`CmdSceneReadyCallback.h` retrieves the player from the active client session, returns if no player is bound, locks the player object, and notifies the associated player object that the scene is ready.

This confirms a scene-ready acknowledgement exists after character entry. The exact client-visible spawn/replication sequence around it still needs tracing.

## Movement/transform serialization

`UpdateTransformMessage.h` serializes:

- a 16-bit marker and 32-bit message identifier;
- a 64-bit scene-object ID;
- three signed 16-bit position components, scaled by four;
- a 32-bit movement counter;
- a speed byte for creatures (zero for non-creatures);
- a direction byte.

The constructor writes coordinates in X, Z, Y order. Its parse method reads three values and passes them to `setPosition(x, y, z)`. Any compatibility implementation must verify coordinate conventions, units, signed range, counter semantics, direction encoding, and the context in which this message is accepted. Do not infer a general movement protocol from this one packet.

## Object-controller framing

`ObjectControllerMessage.h` shows an outer object-controller message with a 16-bit marker, a 32-bit CRC, two 32-bit header values, a 64-bit object ID, and a 32-bit zero field. Compression is configurable.

This reinforces that compatibility requires more than reproducing an opcode: framing, compression, byte order, payload layout, and the nested command registry all matter.

## Security and correctness implications for GalaxyMMO

- Never log passwords, authentication tokens, or raw credential-bearing payloads.
- Do not assume the observed ASCII credential fields are transmitted in cleartext; inspect the actual transport/proxy path before drawing that conclusion.
- GalaxyMMO should use a modern authenticated transport and a password-verifier design appropriate to its identity provider; never copy legacy credential handling without a dedicated security review.
- Character selection must validate account ownership server-side, as the Core3 example does.
- Reconnect and duplicate-session behavior must be explicitly specified and tested.
- Spawn restoration must be modeled as a validated server-side transition, not a client-provided location.
- Movement messages need server-side validation, rate limits, sequence/counter checks, and reconciliation.
- Scene-ready is a state transition that should be idempotent and session-bound.

## Next source-audit targets

1. Trace `BaseClientProxy`, datagram service, packet classes, and crypto/compression layers to establish transport protection and reliability.
2. Trace `LoginPacketHandler` implementations for account lookup, password verification, account ID/session assignment, and zone handoff.
3. Trace `SelectCharacterCallback` callers and the object/baseline messages sent after character insertion.
4. Trace client movement callbacks and the server's authoritative movement validation.
5. Identify object create/destroy, baseline, delta, and containment serializers.
6. Build the upstream revision in a clean supported Linux environment and record actual results.

## Integration recommendation

Continue to keep the GalaxyMMO protocol independent. The source reveals significant domain behavior worth learning from, but the legacy login packet includes credential fields and the zone protocol has specialized state transitions and replication. No direct compatibility or security equivalence is established.
