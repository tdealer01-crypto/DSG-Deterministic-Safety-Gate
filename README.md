# DSG Deterministic Safety Gate

DSG (Deterministic Safety Gate) is an open protocol and reference implementation for deterministic, policy-driven execution systems.

It is designed for game-like control planes where agents behave like players, decisions are auditable, and real-world actions are evaluated through policy invariants and stability scoring.

## Core Concepts

- **Agent** — autonomous unit performing actions
- **Execution** — a request processed by the system
- **Decision** — `ALLOW`, `STABILIZE`, or `BLOCK`
- **Policy Invariant** — rules that must never be violated
- **Stability Score** — computed system safety value between `0.0` and `1.0`
- **Ledger** — audit trail of decisions and actions

## Repository Structure

```text
/protocol
/reference-node
/sdk-python
/sdk-js
/cli
/docs
/examples
/deploy
/.github/workflows
/docker-compose.yml
```

## Included in v0.5

- RFC-0001 protocol skeleton
- JSON schemas for request and decision messages
- Python FastAPI reference node
- configurable policy engine with YAML/JSON policy loading
- persistent SQLite-backed ledger
- API key auth layer for protected endpoints
- Python SDK
- JavaScript SDK
- CLI for execution and inspection
- examples for Python and JavaScript
- GitHub Actions CI workflow
- Kubernetes deploy manifests

## Quick Start

### Local

```bash
cd reference-node
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Docker

```bash
docker compose up --build
```

Then open:
- `http://localhost:8000/docs`
- `http://localhost:8000/health`

Protected endpoints support `x-api-key` when `DSG_API_KEY` is configured.

### Python SDK

```bash
cd sdk-python
pip install -e .
```

### JavaScript SDK

```bash
cd sdk-js
npm install
```

### CLI

```bash
python cli/dsg.py health
python cli/dsg.py execute --agent-id agt_demo --action scan --payload '{"target":"node-1"}'
```

## Vision

DSG turns ordinary dashboards into control planes where:

- agents are visible and operable
- execution is policy-bound
- every decision is inspectable
- safety is computed, not guessed

## Status

`v0.5` — JS SDK, policy files, auth, examples, and k8s manifests added
