# Core API Response Shape

## Goal

Define the stable DSG core response shape required by the customer-facing control-plane.

## Production decision endpoints

### `POST /execute`
Stable production endpoint for the control-plane.

### `POST /evaluate`
Reference compatibility endpoint.
May remain available, but the product shell should standardize on `/execute`.

---

## Required response fields

A successful DSG decision response must include:
- `decision`
- `phase`
- `stability`
- `entropy`
- `proof_hash`
- `ledger_hash`
- `version`
- `evaluated_at`

It should also include either:
- `reason`
or
- `reasons`

Recommended shape:

```json
{
  "decision": "ALLOW",
  "phase": "UNITY",
  "stability": 0.92,
  "entropy": 0.08,
  "proof_hash": "sha256:...",
  "ledger_hash": "sha256:...",
  "version": "0.1.0-beta.1",
  "evaluated_at": "2026-03-28T00:00:00Z",
  "reasons": []
}
```

---

## Decision semantics

### `BLOCK`
Use when:
- hard constraints fail
- forbidden or invalid next state is detected
- replay is detected
- required execution preconditions are missing

### `STABILIZE`
Use when:
- hard constraints pass
- state is not forbidden
- but drift, tuning pressure, or instability exceeds normal allow threshold

### `ALLOW`
Use when:
- state is safe
- stability is acceptable
- no blocking invariant or replay condition is present

---

## Metrics endpoint

### `GET /metrics`
Minimum useful shape:

```json
{
  "allow_count": 0,
  "stabilize_count": 0,
  "block_count": 0,
  "allow_rate": 0,
  "stabilize_rate": 0,
  "block_rate": 0,
  "latest_entropy": 0,
  "latest_stability": 0
}
```

---

## Ledger endpoint

### `GET /ledger`
Must return recent append-only ledger items.

Minimum item fields:
- `id`
- `created_at`
- `decision` or `gate_result`
- `proof_hash`
- `ledger_hash` or chain hash field
- `metadata`

---

## Audit events endpoint

### `GET /audit/events`
Must return recent audit events.

Minimum item fields:
- `sequence`
- `region_id`
- `state_hash`
- `entropy`
- `gate_result`
- `z3_proof_hash` when available
- `created_at`

---

## Determinism endpoint

### `GET /audit/determinism/{sequence}`
Must return:
- `sequence`
- `region_count`
- `unique_state_hashes`
- `max_entropy`
- `deterministic`
- `gate_action`

Recommended shape:

```json
{
  "sequence": 102347,
  "region_count": 3,
  "unique_state_hashes": 1,
  "max_entropy": 0.12,
  "deterministic": true,
  "gate_action": "ALLOW"
}
```

---

## Compatibility rule

The control-plane may adapt field names temporarily, but DSG core should converge on this shape as the stable integration contract.

## Final rule

DSG core is the only production source of `ALLOW`, `STABILIZE`, and `BLOCK`.
