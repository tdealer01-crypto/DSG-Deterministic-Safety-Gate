# Release Notes — DSG v0.1.0-beta.1

Release date: 2026-03-27

## Summary

DSG v0.1.0-beta.1 marks the beta final freeze confirmation for the canonical Python reference stack.
This release establishes the baseline repository structure, reference gate logic, append-only audit ledger, beta final conformance tests, JavaScript SDK scaffold, and CI workflows for validation.

## Included in this release

- `dsg-core` Python package
- `gate.py` canonical decision pipeline
- `harmonics.py` harmonic center and phase evaluation
- `stability.py` drift-to-stability scoring
- `ledger.py` append-only ledger with recompute verification
- `main.py` FastAPI reference node
- `test_beta_final.py` beta final validation suite
- `sdk/js` TypeScript SDK scaffold
- `schemas/request.json` and `schemas/response.json`
- `docs/RFC-0001.md`, `docs/ARCHITECTURE.md`, and `docs/ROADMAP.md`
- GitHub Actions workflows for Python tests and JavaScript SDK build

## Validation status

- Beta final test suite target: 12/12
- Intended status: Run-ready candidate for beta testing
- Scope: Canonical Python reference implementation

## Known limitations

- Replay protection is not yet implemented with an atomic Redis `SET NX EX` pattern
- Distributed nonce storage is not yet implemented
- JavaScript SDK is scaffold-level and intended for beta integration work

## Recommended next steps

1. Run Python beta validation in CI and locally
2. Run JavaScript SDK build in CI and locally
3. Begin external beta testing with controlled users
4. Harden replay protection and nonce storage for release candidate scope
