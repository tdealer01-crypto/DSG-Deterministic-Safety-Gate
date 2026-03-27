# Release Checklist — v0.1.0-beta.1

## Pre-release

- [ ] Confirm `pytest dsg-core/tests/test_beta_final.py -q` passes locally
- [ ] Confirm GitHub Actions workflows pass on `main`
- [ ] Confirm JS SDK build passes locally
- [ ] Review `CHANGELOG.md`
- [ ] Review `docs/RELEASE_NOTES_v0.1.0-beta.1.md`
- [ ] Confirm request and response schemas match runtime behavior
- [ ] Confirm `SECURITY.md`, `LICENSE`, and `NOTICE` are present

## Release

- [ ] Create Git tag `v0.1.0-beta.1`
- [ ] Create GitHub Release using `docs/RELEASE_NOTES_v0.1.0-beta.1.md`
- [ ] Verify release links and repository visibility

## Post-release

- [ ] Monitor beta feedback from users and contributors
- [ ] Track replay-protection hardening work
- [ ] Track distributed nonce storage work
- [ ] Collect issues for `v0.1.0-rc.1`
