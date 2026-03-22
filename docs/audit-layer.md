# Audit Layer

The DSG audit layer extends the execution ledger into region-aware determinism checks.

## Purpose

This layer is designed to support:
- cross-region state alignment
- entropy-aware divergence detection
- state hash comparison
- future proof-oriented audit flows

## Endpoints

### `POST /audit/event`
Ingest a single audit event.

### `GET /audit/events`
List recent audit events.

### `GET /audit/determinism/{sequence}`
Compute determinism for a specific sequence across all submitted regions.

## Current Determinism Rule

For a given sequence:
- collect all `state_hash` values
- compute `max_entropy`
- mark as deterministic only if:
  - there is at most one unique state hash
  - max entropy is below `1.0`

If not deterministic, the recommended gate action is `FREEZE`.

## Example Event

```json
{
  "epoch": "GEN5-EPOCH-001",
  "sequence": 102347,
  "region_id": "asia-southeast1",
  "state_hash": "9fa3e21",
  "entropy": 0.83,
  "gate_result": "ALLOW",
  "z3_proof_hash": "a9f321c",
  "signature": "ed25519:..."
}
```
