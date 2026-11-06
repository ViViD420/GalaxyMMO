# GalaxyMMO

GalaxyMMO is an original open-world sandbox MMORPG project. The planned client is Unreal Engine 5 + C++; SWGEmu Core3 is the intended existing server foundation, with a compatibility-first strategy that preserves working upstream systems and changes only what GalaxyMMO demonstrably requires.

**Project phase:** foundation and Core3 integration reconnaissance.

## Start here

- [Architecture](docs/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)
- [Core3 integration plan](docs/CORE3_INTEGRATION_PLAN.md)
- [Core3 feature reuse matrix](docs/CORE3_FEATURE_REUSE_MATRIX.md)
- [Core3 reconnaissance](docs/CORE3_RECONNAISSANCE.md)
- [Client/server protocol boundary](docs/PROTOCOL_BOUNDARY.md)
- [Authentication/session contract draft](Integration/Contracts/auth-session-v0.1.md)
- [Development environment](docs/DEVELOPMENT_ENVIRONMENT.md)
- [Contribution guide](CONTRIBUTING.md)
- [Legal and third-party notices](LEGAL_NOTICES.md)

## Engineering principles

- Preserve Core3's working systems wherever they meet requirements.
- Prefer configuration, data, scripts, and supported extension points over core rewrites.
- Keep GalaxyMMO client-facing contracts independent of Core3 internals.
- Server-authoritative gameplay and persistence.
- Explicit, versioned client/server contracts.
- Never claim compatibility or successful builds without repeatable proof.
- Original project-owned setting, names, art, audio, and game content.
- Automated validation and tests from the beginning.

## Current validation

Run from the repository root with Python 3.12 or compatible:

```sh
python tools/validate_protocol.py
python -m unittest discover -s tests -v
```

The current protocol manifest is design metadata only; transport, serialization, and wire messages remain undecided.

## Important

No proprietary client executable, extracted commercial game assets, or client data are included. Review [LEGAL_NOTICES.md](LEGAL_NOTICES.md) before integrating third-party code or data.
