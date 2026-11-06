# ADR-0003: Preserve Core3 as the Existing Server Foundation

- **Status:** Accepted as the working project direction; subject to build and integration proof
- **Date:** 2026-11-06

## Context

GalaxyMMO is intended to build on the existing SWGEmu Core3 server foundation. Core3 already contains substantial server runtime, networking, session, object, gameplay, and persistence systems. Replacing those systems wholesale would add risk and duplicate mature behavior.

GalaxyMMO also requires an original Unreal Engine client, original game content, and project-specific gameplay changes. Core3's existing client protocol and runtime assumptions cannot be presumed to match that client.

## Decision

1. Keep the upstream Core3 codebase as the baseline server implementation.
2. Prefer configuration, scripts, data definitions, and narrow extension points before modifying core C++.
3. Keep GalaxyMMO-owned adapters and new services in separately identifiable modules.
4. When a Core3 core change is unavoidable, make the smallest isolated patch, document why it is required, and add a regression test or reproducible validation.
5. Track the exact upstream commit used by each integration branch. Do not silently mix upstream revisions.
6. Do not replace Core3 networking or persistence merely because GalaxyMMO has a new client. First evaluate a gateway or adapter that translates a stable GalaxyMMO contract into Core3 operations.
7. Never claim the integration works until the actual build and end-to-end proof have been run.

## Change classification

| Change class | Default treatment |
|---|---|
| Existing Core3 feature already meets the requirement | Reuse unchanged |
| Content, tuning, or configuration | Prefer data/configuration changes |
| New gameplay behavior with supported extension point | Add isolated extension |
| New client protocol | Add a gateway/adapter boundary first |
| Core3 defect blocking the requirement | Minimal upstream patch plus regression test |
| Fundamental incompatibility proven by a test | Reconsider only the affected subsystem |

## Consequences

- Core3 remains the authoritative owner of systems it already implements successfully.
- GalaxyMMO-specific behavior remains easier to review, upgrade, and rebase.
- The Unreal client does not need to know Core3 internal classes or packet layouts.
- Some integration decisions remain open until a clean Core3 build and network lifecycle audit are complete.

## Revisit when

- A clean build reveals unsupported or broken upstream dependencies.
- A required GalaxyMMO feature cannot be implemented through supported extension points.
- A gateway proof of concept demonstrates unacceptable latency, complexity, or correctness.
- An upstream change materially alters the audited networking or persistence paths.
