# GalaxyMMO

GalaxyMMO is an original open-world sandbox MMORPG project. The planned client is Unreal Engine 5 + C++; SWGEmu Core3 is being evaluated as a possible server foundation, not assumed to be a drop-in backend.

**Project phase:** foundation and technical reconnaissance.

## Start here

- [Architecture](docs/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)
- [Development environment](docs/DEVELOPMENT_ENVIRONMENT.md)
- [Core3 reconnaissance plan](docs/CORE3_RECONNAISSANCE.md)
- [Client/server protocol boundary](docs/PROTOCOL_BOUNDARY.md)
- [Contribution guide](CONTRIBUTING.md)
- [Legal and third-party notices](LEGAL_NOTICES.md)

## Engineering principles

- Server-authoritative gameplay and persistence.
- Explicit, versioned client/server contracts.
- Core3 compatibility is not claimed until verified by source audit and a repeatable proof of concept.
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
