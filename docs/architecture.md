# Architecture

DSG is organized around six layers:

1. **Protocol Layer**
   - RFC-0001
   - JSON schemas
   - OpenAPI export

2. **Control Plane Layer**
   - operator-facing dashboards and command interfaces
   - integration surface for agent monitoring, billing, auth, and policy operations

3. **Execution Layer**
   - FastAPI reference node
   - `/execute`, `/ledger`, `/health`, `/metrics`

4. **Policy Layer**
   - action classification into `ALLOW`, `STABILIZE`, `BLOCK`
   - YAML/JSON policy file loading
   - policy validation helpers

5. **Persistence + Audit Layer**
   - SQLite by default
   - PostgreSQL-compatible connection path scaffold
   - deterministic ledger for auditability

6. **Developer Tooling Layer**
   - Python SDK
   - JavaScript SDK
   - CLI
   - CI and release workflows

## Data Flow

1. Client submits execution request
2. Auth layer validates `x-api-key` if configured
3. Policy engine evaluates action and computes decision
4. Ledger persists execution result
5. Control plane or SDK reads the resulting state
6. Client receives auditable response

## Ecosystem Alignment

DSG can be deployed as a standalone execution gate, but it is designed to sit inside a larger ecosystem:
- control plane for operator UX
- audit engine for deterministic state verification
- governance layer for legal, research, and policy framing
