from fastapi import Depends, FastAPI

from .auth import require_api_key
from .audit import get_determinism, list_audit_events, record_audit_event
from .database import init_db
from .ledger import list_entries, metrics as ledger_metrics, record_execution
from .models import AuditEventRequest, ExecutionRequest
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
        "database": "sqlite" if settings.is_sqlite else "postgresql",
    }


@app.get("/metrics", dependencies=[Depends(require_api_key)])
def metrics() -> dict:
    return ledger_metrics()


@app.post("/execute", dependencies=[Depends(require_api_key)])
def execute(req: ExecutionRequest) -> dict:
    decision = evaluate_execution(req)
    entry = record_execution(req, decision)
    return {
        **decision.model_dump(),
        "ledger_entry": entry,
    }


@app.get("/ledger", dependencies=[Depends(require_api_key)])
def ledger() -> dict:
    return {"items": list_entries()}


@app.post("/audit/event", dependencies=[Depends(require_api_key)])
def ingest_audit_event(event: AuditEventRequest) -> dict:
    entry = record_audit_event(event)
    return {"ok": True, "item": entry}


@app.get("/audit/events", dependencies=[Depends(require_api_key)])
def audit_events(limit: int = 50) -> dict:
    return {"items": list_audit_events(limit=limit)}


@app.get("/audit/determinism/{sequence}", dependencies=[Depends(require_api_key)])
def audit_determinism(sequence: int) -> dict:
    result = get_determinism(sequence)
    return result.model_dump()
