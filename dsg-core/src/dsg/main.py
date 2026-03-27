from fastapi import FastAPI

from .gate import DSGGate, DSGRequest

app = FastAPI(title="DSG Reference Node", version="0.1.0-beta.1")
gate = DSGGate()


@app.get("/health")
def health() -> dict:
    return {
        "status": "DSG_ACTIVE",
        "deterministic": True,
        "version": "0.1.0-beta.1",
    }


@app.post("/evaluate")
def evaluate(req: DSGRequest):
    return gate.process_request(req)


@app.get("/ledger/verify")
def verify_ledger() -> dict:
    return {"ok": gate.ledger.verify_chain(), "entries": len(gate.ledger.chain)}
