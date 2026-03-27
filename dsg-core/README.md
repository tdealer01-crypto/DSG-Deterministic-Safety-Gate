# dsg-core

Canonical Python reference stack for DSG v0.1.0-beta.1.

## Install

```bash
pip install -e .[dev]
```

## Run tests

```bash
pytest tests/test_beta_final.py -q
```

## Run reference node

```bash
uvicorn dsg.main:app --reload
```
