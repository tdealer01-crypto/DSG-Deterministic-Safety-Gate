# Security Policy

## Supported versions

The current beta support target is:

- `v0.1.0-beta.1`

Earlier versions may not receive fixes.

## Reporting a vulnerability

Please report security issues privately before opening a public issue.
Include as much detail as possible:

- affected version
- component or file involved
- reproduction steps
- expected impact
- logs or traces if available

## Scope notes

Known hardening gaps for the current beta include:

- atomic replay protection is not yet implemented
- distributed nonce storage is not yet implemented
- beta SDK integrations may require environment-specific adjustments

## Response expectations

Security reports will be triaged first for reproducibility and protocol impact.
Where possible, fixes should be accompanied by regression tests and documentation updates.
