# DSG Deterministic Safety Gate

DSG (Deterministic Safety Gate) is an open protocol and reference implementation for deterministic, policy-driven execution systems.

It is designed for game-like control planes where agents behave like players, decisions are auditable, and real-world actions are evaluated through policy invariants and stability scoring.

## Core Concepts

- **Agent** — autonomous unit performing actions
- **Execution** — a request processed by the system
- **Decision** — `ALLOW`, `STABILIZE`, or `BLOCK`
- **Policy Invariant** — rules that must never be violated
- **Stability Score** — computed system safety value between `0.0` and `1.0`
- **Ledger** — audit trail of decisions and actions

## Repository Structure

```text
/protocol
/reference-node
```

## Initial Scope

This repository starts with:

- RFC-0001 protocol skeleton
- Python FastAPI reference node
- basic execution endpoint with deterministic decision output

## Vision

DSG turns ordinary dashboards into control planes where:

- agents are visible and operable
- execution is policy-bound
- every decision is inspectable
- safety is computed, not guessed

## Status

`v0.1` — initial scaffold
