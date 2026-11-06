# Client/Server Protocol Boundary

## Goal

Keep the Unreal client independent of Core3 implementation details and make the wire contract explicit, versioned, and testable.

## Rules

- The client sends commands expressing player intent; the server returns authoritative results and state updates.
- Every message has a protocol version, message type, and bounded payload.
- Authentication credentials and session tokens must never be written to logs.
- Reject unknown required fields, unsupported protocol versions, malformed payloads, oversized messages, and commands from the wrong session.
- Define stable identifiers for entities and items; never use client memory addresses or transient array indexes as identity.
- Design retries deliberately. Mutating commands should carry an idempotency identifier.
- Do not select a serialization library or transport until latency, compatibility, security, and operational requirements are measured.

## Initial contract status

`Integration/Protocol/protocol-manifest.json` is metadata only. It is not a finalized wire format and does not imply compatibility with Core3. The actual message schema will be added after the Core3 network reconnaissance and client vertical-slice requirements are complete.
