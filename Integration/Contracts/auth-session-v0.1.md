# Authentication and Session Contract — Draft 0.1

- **Status:** Draft; not a wire protocol
- **Audience:** Unreal client, GalaxyMMO gateway/adapter, server integration
- **Core3 mapping:** Not yet established

## Purpose

Define the responsibilities and lifecycle that an authentication integration must satisfy without prematurely selecting HTTP, WebSocket, TCP, UDP, a serialization library, or a credential-storage implementation.

## Security requirements

- Credentials are submitted only over an authenticated, encrypted channel.
- Passwords are never logged, placed in analytics, or returned to the client.
- Password storage must use a modern, purpose-built password hashing scheme with per-password salts and parameters selected for the deployment; never store plaintext or reversible password encryption.
- Session credentials are high-entropy, opaque, revocable, and transmitted only over the protected channel.
- Session secrets are not written to logs, crash reports, or client-visible error messages.
- Authentication attempts are rate-limited and monitored without revealing whether an account exists.
- Account state, bans, entitlements, and character ownership are checked server-side.
- Secrets and database credentials are supplied through deployment secret management, not committed configuration files.

These are requirements, not a claim that Core3 currently implements this exact contract. Core3's credential protection and session handoff must be traced and tested before choosing whether its existing authentication path can be reused.

## Lifecycle

1. **Client hello:** client identifies its supported GalaxyMMO contract version and build identifier. No credentials are sent before secure transport is established.
2. **Authentication request:** client submits account identifier and credential proof through the selected secure authentication mechanism.
3. **Authentication result:** server returns a generic success/failure outcome. On success it issues an opaque session credential and a server-defined expiry.
4. **Character listing:** client requests characters associated with that authenticated account. The server derives account identity from the session, never from a client-supplied account ID.
5. **Character selection:** client submits a stable character identifier. Server verifies ownership, availability, and account/session status.
6. **World entry:** server establishes the world session and returns the initial authoritative state required by the client.
7. **Reconnect:** client presents the valid session credential or reauthenticates. Server revalidates account and character state; reconnect must not create duplicate active control of a character.
8. **Logout/revocation:** server invalidates the session and releases active world control using a defined timeout and cleanup policy.

## Required error categories

- unsupported_protocol
- invalid_credentials
- account_unavailable
- account_restricted
- session_expired
- session_revoked
- character_unavailable
- rate_limited
- temporarily_unavailable
- internal_error

Client-facing messages should not disclose sensitive account state. Diagnostic details belong in protected server logs with credentials and tokens redacted.

## Invariants

- A session belongs to exactly one authenticated account.
- A selected character must belong to that account.
- A character cannot be controlled by two active sessions unless an explicit, tested handoff policy permits it.
- Every state-changing request is authorized against the active session and server-side character state.
- Duplicate authentication or character-selection messages must not produce duplicate world ownership.
- Session expiry and disconnect cleanup are server-authoritative.

## Open decisions

- Transport and cryptographic handshake.
- Whether authentication is handled directly by Core3, by a gateway, or by a GalaxyMMO identity service.
- Password verification and migration strategy for any existing Core3 account database.
- Session token format, storage, rotation, expiry, and revocation.
- Multi-factor authentication and account recovery requirements.
- Exact request/response serialization and version negotiation.

## Acceptance tests required before implementation is called complete

- Reject credentials over an unencrypted connection.
- Ensure logs and error messages contain no credential or token values.
- Verify account ownership and character ownership checks.
- Reject expired, revoked, malformed, and wrong-account sessions.
- Reject duplicate active character control and test reconnect cleanup.
- Apply rate limits without account-enumeration leaks.
- Test version mismatch and malformed/oversized payload handling.
