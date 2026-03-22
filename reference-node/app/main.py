from fastapi import FastAPI

from .database import init_db
from .ledger import list_entries, metrics as ledger_metrics, record_execution
from .models import ExecutionRequest
from .policy import evaluate_execution
from .settings import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/")
def root() -> dict:
    return {
        "status": "DSG Node Online",
        "service": "reference-node",
        "version": settings.app_version,
    }


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "database": "sqlite",
    }


@app.get("/metrics")
def metrics() -> dict:
    return ledger_metrics()


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
