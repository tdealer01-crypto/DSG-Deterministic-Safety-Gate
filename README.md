# DSG Deterministic Safety Gate

DSG v0.1.0-beta.1 is the Beta Canonical Reference Implementation for the DSG protocol.

## Status

- Version: `v0.1.0-beta.1`
- Stage: Beta Testing
- Scope: Canonical Python reference stack
- Validation: 12/12 beta final tests passed

## Repository layout

- `dsg-core/` - Python core engine, gate logic, ledger, tests
- `sdk/js/` - TypeScript SDK
- `schemas/` - Canonical request/response schemas
- `docs/` - RFC, architecture, roadmap

## Quick start

```bash
pip install -e ./dsg-core[dev]
pytest dsg-core/tests/test_beta_final.py -q
```

## Developer notice

DSG v0.1.0-beta.1 has passed beta final freeze validation for the canonical Python reference stack.
Production hardening remains pending on atomic replay protection and distributed nonce storage.
