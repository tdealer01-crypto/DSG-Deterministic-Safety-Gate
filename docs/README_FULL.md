# DSG Deterministic Safety Gate

![DSG Beta Final Tests](https://github.com/tdealer01-crypto/DSG-Deterministic-Safety-Gate/actions/workflows/python-tests.yml/badge.svg)
![DSG JS SDK Build](https://github.com/tdealer01-crypto/DSG-Deterministic-Safety-Gate/actions/workflows/js-sdk-build.yml/badge.svg)
![DSG Python Smoke Test](https://github.com/tdealer01-crypto/DSG-Deterministic-Safety-Gate/actions/workflows/python-smoke-test.yml/badge.svg)

DSG v0.1.0-beta.1 is the Beta Canonical Reference Implementation for the DSG protocol.
This repository contains the canonical Python reference stack, a JavaScript SDK scaffold, protocol schemas, documentation, and CI workflows for beta validation.

## Status

- Version: `v0.1.0-beta.1`
- Stage: Beta Testing
- Scope: Canonical Python reference stack
- Validation target: 12/12 beta final cases
- Current use: run-ready candidate for controlled beta testing

## Repository layout

- `dsg-core/` - Python engine, gate logic, ledger, reference node, and tests
- `sdk/js/` - TypeScript SDK scaffold
- `schemas/` - canonical request and response schemas
- `docs/` - RFC, architecture, roadmap, release notes, and launch checklists
- `examples/` - simple usage examples

## Quick start

### Python core

```bash
pip install -e ./dsg-core[dev]
pytest dsg-core/tests/test_beta_final.py -q
uvicorn dsg.main:app --reload
```

### JavaScript SDK

```bash
cd sdk/js
npm install
npm run build
```

## What is included in beta.1

- version gating
- replay incident detection
- Makk-8 core invariant enforcement
- harmonic phase evaluation
- stability scoring
- canonical proof binding
- append-only ledger with recompute verification
- Python beta validation suite
- JavaScript SDK scaffold
- GitHub Actions workflows for Python tests, JS build, and Python smoke testing

## Documentation

- `docs/RFC-0001.md`
- `docs/ARCHITECTURE.md`
- `docs/ROADMAP.md`
- `docs/RELEASE_NOTES_v0.1.0-beta.1.md`
- `docs/RELEASE_CHECKLIST.md`
- `docs/LAUNCH_CHECKLIST.md`

## Security and hardening notes

This repository is ready for beta testing, not production hardening.
Known gaps still include:

- replay protection is not yet atomic (`GET` + `SETEX` instead of `SET NX EX`)
- distributed nonce storage is not yet implemented
- JavaScript SDK is scaffold-level and intended for beta integration work

## Community files

This repository includes:

- `LICENSE`
- `NOTICE`
- `SECURITY.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- issue templates and pull request template

## Recommended next steps

1. Verify all GitHub Actions workflows pass on `main`
2. Create the Git tag `v0.1.0-beta.1`
3. Create a GitHub Release using `docs/RELEASE_NOTES_v0.1.0-beta.1.md`
4. Start controlled external beta testing
5. Harden replay protection and nonce storage for the next release candidate
