# Changelog

All notable changes to this repository will be documented in this file.

## [0.1.0-beta.1] - 2026-03-27

### Added
- Canonical Python reference stack under `dsg-core/`
- Deterministic gate pipeline with version gating, replay detection, Makk-8 invariant checks, harmonic phase evaluation, stability scoring, proof binding, and append-only ledger commits
- Append-only audit ledger with recompute-based tamper verification
- FastAPI reference node entrypoint
- Beta final conformance tests under `dsg-core/tests/test_beta_final.py`
- JavaScript SDK scaffold under `sdk/js/`
- Canonical JSON schemas for request and response payloads
- Initial documentation set: RFC-0001, architecture overview, roadmap, and repository README
- GitHub Actions workflows for Python beta tests and JavaScript SDK build

### Notes
- This release is intended for beta testing of the canonical Python reference stack.
- Production hardening remains pending on atomic replay protection and distributed nonce storage.
