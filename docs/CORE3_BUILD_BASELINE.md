# Core3 Build Baseline

## Purpose and current pin

This document defines a reproducible first build attempt for the upstream Core3 server. It does not claim that GalaxyMMO has built Core3 yet.

- Upstream: https://github.com/swgemu/Core3
- Audited source pin: `403893d9b9f8e6fa712fbb3cb1fcd8f0fe45bb79`
- Branch context at inspection: `unstable`
- Required policy: keep this checkout separate from the GalaxyMMO repository.
- Build state: **not yet executed by GalaxyMMO**.

The pin is the source snapshot used for the current reconnaissance. It is not represented as the latest upstream commit.

## Documented build environment

The upstream README currently describes Debian 12 and lists CMake 3.18+, Berkeley DB 5.3, MariaDB client/server, OpenSSL, pthreads, Lua 5.3, zlib, clang 19, Java runtime, Boost, and Ninja. It documents a development build using `make build-ninja-debug` from `MMOCoreORB`, and a production build using `make -j$(nproc)`.

Source: https://github.com/swgemu/Core3/blob/unstable/README.md

Always re-check the README and build scripts at the exact pinned revision before provisioning. Dependency package names and compiler requirements can change upstream.

## Separate checkout

Example layout:

```text
workspace/
  GalaxyMMO/       # this project
  Core3/           # upstream checkout, separately pinned
```

Clone the upstream repository:

```sh
mkdir -p ~/workspace
cd ~/workspace
git clone https://review.swgemu.com/Core3
cd Core3
git checkout 403893d9b9f8e6fa712fbb3cb1fcd8f0fe45bb79
```

If the official clone endpoint changes, use the upstream repository's current documented clone URL. Do not substitute an unreviewed fork.

## Verify the checkout before building

From the GalaxyMMO repository root:

```sh
python tools/check_core3_checkout.py ../Core3
```

The checker is read-only. It confirms the expected Git remote, exact audited commit, and clean working tree. It does not verify dependencies, compilation, database setup, runtime data, or server behavior.

## Development build attempt

On a clean Debian 12 environment with dependencies installed according to the pinned upstream instructions:

```sh
cd ~/workspace/Core3/MMOCoreORB
make build-ninja-debug
```

Capture the complete command output and exit code. Record OS image, compiler version, CMake version, dependency versions, and any environment overrides. Do not copy generated build products into GalaxyMMO source control.

## Runtime and data prerequisites

A successful compile is not a successful server startup. Core3's documented Docker setup expects client `.tre` data to be supplied separately for runtime use. GalaxyMMO must not commit proprietary client archives or extracted content. Runtime testing must use data the operator is authorized to use and must record exactly which prerequisites were present.

Database setup, schema import, configuration, and runtime smoke tests should be performed only in an isolated development environment with non-production credentials. Never commit passwords, database dumps containing personal data, or local configuration secrets.

## Acceptance record

Update this table only with observed results:

| Check | Status | Evidence |
|---|---|---|
| Pinned clean checkout | Not run | Run checkout checker |
| Debian/toolchain versions recorded | Not run | Attach build log or issue |
| Debug build | Not run | Exit code and complete log |
| Database initialized | Not run | Sanitized setup record |
| Server startup smoke test | Not run | Sanitized startup log |
| Login/zone smoke test | Not run | Test procedure and result |

## Failure handling

- Do not patch Core3 just to work around an unverified local dependency mismatch.
- First compare the environment with the pinned upstream build instructions.
- Keep any necessary compatibility patch in a separately reviewable patch series.
- Add a regression test for a real source defect before considering the patch complete.
