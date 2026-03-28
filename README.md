# DSG Deterministic Safety Gate

[![CI](https://github.com/tdealer01-crypto/DSG-Deterministic-Safety-Gate/actions/workflows/core-ci.yml/badge.svg)](https://github.com/tdealer01-crypto/DSG-Deterministic-Safety-Gate/actions/workflows/core-ci.yml)

DSG is the canonical reference implementation of the Deterministic Safety Gate protocol.

## Structure
- dsg-core/
- sdk/js/
- schemas/
- docs/

## Quick Start
pip install -e ./dsg-core[dev]
pytest dsg-core/tests/test_beta_final.py -q

## Dev
cd dsg-core && make install && make test && make lint && make format