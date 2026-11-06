# Development Environment

## Current constraints

The Unreal Editor, asset pipeline, C++ client builds, profiling, and packaged-client testing require a suitable Windows/Linux desktop or remote workstation. A phone can review files, manage issues, and use browser-based GitHub tools, but it is not a practical substitute for the Unreal desktop toolchain.

## Server investigation

Core3 upstream documents a Docker-based environment and a Debian 12 manual build path. The manual path lists CMake 3.18+, Berkeley DB 5.3, MariaDB, OpenSSL, pthreads, Lua 5.3, zlib, clang 19, Java runtime, Boost, and Ninja. Confirm exact dependencies against the pinned upstream revision before provisioning.

Upstream build guide: https://github.com/swgemu/Core3

## Suggested Windows workstation path

1. Install a supported 64-bit Windows version and current Windows updates.
2. Install WSL2 with Ubuntu and enable WSL integration in Docker Desktop.
3. Install Git and a C++ IDE/toolchain supported by the selected Unreal Engine release.
4. Clone GalaxyMMO and Core3 into separate working directories.
5. Follow Core3's current WSL2/Docker instructions for the server evaluation; do not assume an old command still matches the current branch.
6. Install the matching Unreal Engine version and create the client project only after selecting the client architecture.

## Remote development

GitHub Codespaces can support repository editing and some Linux build/test work, subject to account availability, machine size, and billing. It does not replace a full Unreal Editor workstation for world authoring and visual debugging. Do not upload client data or secrets to an untrusted remote environment.

## Reproducibility

Record tool versions, commands, environment variables (never secret values), and outcomes in `docs/` or issue discussions. Prefer pinned versions and automated checks over undocumented local setup.
