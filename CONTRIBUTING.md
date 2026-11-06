# Contributing to GalaxyMMO

## Working principles

- Keep changes focused and reviewable.
- Prefer small pull requests with a clear problem statement and verification notes.
- Do not commit credentials, private keys, access tokens, local database dumps, or proprietary game assets.
- Do not claim a feature is tested unless the test was actually run; include commands and results.
- Add or update tests when changing validation, persistence, protocol contracts, or game rules.
- Record material architecture decisions as ADRs in `docs/decisions/`.

## Branch and commit conventions

Use descriptive branches such as `feature/inventory-contract` or `fix/protocol-validation`. Use concise imperative commit messages, optionally prefixed with `feat:`, `fix:`, `docs:`, `test:`, `build:`, or `chore:`.

## Pull request checklist

- [ ] Scope and behavior are explained.
- [ ] Tests or validation commands are listed with actual results.
- [ ] Documentation and protocol versions are updated where applicable.
- [ ] No secrets, copyrighted assets, generated build output, or unrelated files are included.
- [ ] Server-side validation remains authoritative for consequential state.
