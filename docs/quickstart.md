# Quick Start

## Run locally

```bash
cd reference-node
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:
- `http://localhost:8000/`
- `http://localhost:8000/docs`
- `http://localhost:8000/ledger`

## Run with Docker

```bash
docker compose up --build
```

## Test execution

```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agt_demo",
    "action": "scan",
    "payload": {"target": "node-1"}
  }'
```
