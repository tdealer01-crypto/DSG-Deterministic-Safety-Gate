# Contributing to DSG Deterministic Safety Gate

Thank you for contributing to DSG.

## Principles

Contributions should preserve:

- deterministic behavior
- auditability
- protocol fidelity
- testability

## Development flow

1. Fork the repository or create a working branch
2. Make focused changes
3. Add or update tests
4. Run the local validation steps
5. Open a pull request with a clear summary

## Local validation

### Python core

```bash
pip install -e ./dsg-core[dev]
pytest dsg-core/tests/test_beta_final.py -q
```

### JavaScript SDK

```bash
cd sdk/js
npm install
npm run build
```

## Pull request expectations

Please include:

- what changed
- why it changed
- whether protocol behavior changed
- what tests were added or updated
- any known limitations

## Scope guidance

Good contribution areas:

- protocol conformance tests
- replay protection hardening
- distributed nonce storage
- SDK improvements
- documentation and examples

Avoid mixing unrelated refactors with protocol changes in the same pull request.

## Security notes

Do not commit secrets, credentials, or private environment values.
If you identify a security issue, report it privately before opening a public issue or PR.
