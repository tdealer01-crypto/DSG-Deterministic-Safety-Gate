# Release

## Versioning

The repository tracks its current release target in the `VERSION` file.

## Release Inputs

Before creating a real public release, verify:
- `CHANGELOG.md` is updated
- `VERSION` matches the intended release
- `protocol/openapi.json` is regenerated if API changed
- CI is passing
- policy schemas and examples still match runtime behavior

## Publish Direction

### Python SDK
Recommended next step:
- rename package if needed for PyPI uniqueness
- publish from `sdk-python`

### JavaScript SDK
Recommended next step:
- add package publishing metadata
- publish from `sdk-js`

## Release Workflow

The current `release.yml` is a scaffold.
Expand it to:
- build SDK artifacts
- create git tags
- generate release notes
- publish packages
- attach OpenAPI and schema artifacts
