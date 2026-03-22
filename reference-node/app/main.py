from fastapi import FastAPI

from .ledger import list_entries, record_execution
from .models import ExecutionRequest
from .policy import evaluate_execution

app = FastAPI(title="DSG Reference Node", version="0.2.0")


@app.get("/")
def root() -> dict:
    return {
        "status": "DSG Node Online",
        "service": "reference-node",
        "version": "0.2.0",
    }


@app.post("/execute")
def execute(req: ExecutionRequest) -> dict:
    decision = evaluate_execution(req)
    entry = record_execution(req, decision)
    return {
        **decision.model_dump(),
        "ledger_entry": entry,
    }


@app.get("/ledger")
def ledger() -> dict:
    return {"items": list_entries()}
