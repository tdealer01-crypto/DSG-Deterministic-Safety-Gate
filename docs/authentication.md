# Authentication

DSG supports optional API key protection for operational endpoints.

## Modes

### 1. No API key configured
If neither `DSG_API_KEY` nor `DSG_API_KEYS` is set, protected endpoints remain open for local development.

### 2. Single key
Set:

```bash
export DSG_API_KEY=your-secret-key
```

Then send:

```http
x-api-key: your-secret-key
```

### 3. Multiple keys
Set:

```bash
export DSG_API_KEYS=key-one,key-two,key-three
```

This is useful when:
- multiple operators need distinct shared keys
- services and humans use separate credentials
- staging and automation need different access tokens

## Protected Endpoints

The following endpoints are protected when API keys are configured:
- `POST /execute`
- `GET /ledger`
- `GET /metrics`

## Recommended Evolution

Current auth is intentionally simple.

For production hardening, extend toward:
- hashed API keys in persistent storage
- key metadata and owner labels
- rotation and revocation
- scoped permissions for read vs execute
- org-level auth mapped from the control plane
