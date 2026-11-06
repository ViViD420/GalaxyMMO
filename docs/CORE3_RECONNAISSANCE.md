# Core3 Reconnaissance Plan

## Current finding

The upstream `swgemu/Core3` README describes a server emulator targeting the classic SWG Pre-CU environment. It documents a Docker-based development path and a Linux build path. The documented manual-build dependencies include Debian 12, CMake 3.18+, Berkeley DB 5.3, MariaDB, OpenSSL, pthreads, Lua 5.3, zlib, clang 19, a Java runtime, Boost, and Ninja. These are upstream README statements, not a verified build on this project yet.

Upstream: https://github.com/swgemu/Core3

## Questions to answer before integration

1. What branch and commit are we evaluating, and what license applies to that exact revision?
2. Where are login, authentication, session lifecycle, message dispatch, object creation/destruction, and replication implemented?
3. Which transport, framing, encryption, compression, and message serialization rules does the original client expect?
4. Which server systems can be reused without inheriting assumptions that conflict with GalaxyMMO's original design?
5. What client data files are required at runtime, and what rights are required to use them?
6. Can an adapter expose a stable, documented API without patching deep Core3 internals?

## Required deliverables

- Pin the evaluated upstream commit SHA and record it here.
- Produce a dependency/build report from a clean environment.
- Map authentication and session flow with source file paths and call sequence.
- Map object lifecycle and replication with source file paths and message names.
- Identify licensing obligations and any asset/data prerequisites.
- Build a minimal integration spike before selecting direct protocol, gateway, or replacement service architecture.

## Current status

**Not yet audited or built.** No compatibility claim is made. Do not copy proprietary client binaries, extracted game assets, or copyrighted game content into this repository.
