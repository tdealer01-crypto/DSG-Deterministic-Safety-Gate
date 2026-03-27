# DSG Architecture

## Core components

- `dsg-core/src/dsg/gate.py` - decision pipeline and proof binding
- `dsg-core/src/dsg/harmonics.py` - harmonic center and phase analysis
- `dsg-core/src/dsg/stability.py` - drift-to-stability scoring
- `dsg-core/src/dsg/ledger.py` - append-only audit ledger with recompute verification
- `dsg-core/src/dsg/main.py` - FastAPI reference node

## Decision pipeline

1. Version gating
2. Replay detection
3. Makk-8 invariant verification
4. Harmonic phase evaluation
5. Stability scoring
6. Decision assignment
7. Proof hash generation
8. Ledger commit

## Current scope

This repository is the canonical Python reference stack for DSG beta.1.
Production hardening for atomic replay protection and distributed nonce storage remains out of scope for this beta release.
