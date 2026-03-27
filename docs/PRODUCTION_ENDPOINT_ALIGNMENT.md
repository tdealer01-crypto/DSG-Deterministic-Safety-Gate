# Production Endpoint Alignment

## Goal

Align DSG core with the endpoints already expected by the customer-facing control-plane.

## Current reference node

Current routes:
- `GET /health`
- `POST /evaluate`
- `GET /ledger/verify`

## Required production routes

The product shell expects these routes:
- `POST /execute`
- `GET /metrics`
- `GET /ledger`
- `GET /audit/events`
- `GET /audit/determinism/{sequence}`

## Required behavior

### POST /execute
Purpose:
- main production decision endpoint

Input should support the current control-plane bridge while preserving deterministic DSG semantics.

Minimum output fields:
- `decision`
- `reason` or `reasons`
- `proof_hash`
- `ledger_hash`
- `stability`
- `entropy`
- `version`
- `evaluated_at`

### GET /metrics
Purpose:
- expose live gate-level metrics for Mission Control

Minimum fields:
- decision counts
- allow rate
- stabilize rate
- block rate
- latest stability summary
- latest entropy summary

### GET /ledger
Purpose:
- return recent append-only ledger items for operator visibility

### GET /audit/events
Purpose:
- return recent audit events for dashboard and audit explorer

### GET /audit/determinism/{sequence}
Purpose:
- return determinism status for a given sequence

Minimum fields:
- `sequence`
- `region_count`
- `unique_state_hashes`
- `max_entropy`
- `deterministic`
- `gate_action`

## Compatibility rule

- keep `POST /evaluate` for reference compatibility
- add `POST /execute` as the stable production contract
- keep `GET /health`
- keep `GET /ledger/verify` as an integrity utility endpoint

## Product rule

DSG core is the only production source of:
- `ALLOW`
- `STABILIZE`
- `BLOCK`

No second decision engine is allowed in the customer-facing product path.

## Definition of done

Alignment is complete when:
1. control-plane can call DSG core without endpoint translation hacks
2. dashboard health is live from DSG core
3. audit page is live from DSG core
4. ledger page is live from DSG core
5. determinism checks are live from DSG core
6. all production decisions come from DSG core only
