# Verified DSG Core

This directory records the uploaded formal verification artifact that has already been independently verified for the DSG gate core.

## Verified properties

The verified DSG gate core establishes these properties:

- Determinism
- Safety invariance
- Constant-time bound

## Artifact

- SMT-LIB v2 proof: `artifacts/formal/dsg_full_proof.smt2`
- Solver: Z3
- Expected result: `sat`

## Reproduction

```bash
z3 artifacts/formal/dsg_full_proof.smt2
```

## Scope boundary

These files verify the formal DSG gate core only.

They do **not** by themselves verify:

- runtime orchestration
- monitor pipelines
- billing or organization flows
- product assembly across multiple repositories
- external actuator or world-interface integrations

Those areas still need to be checked against repository implementation truth.
