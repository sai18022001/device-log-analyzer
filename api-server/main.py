from fastapi import FastAPI, Query
from typing import Optional, List
from database import SessionLocal, LogRecord, init_db
from models import LogResponse, SummaryItem
from sqlalchemy import func, Integer, case

app = FastAPI(title="Device Log Analyzer API")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/logs", response_model=List[LogResponse])
def get_logs(
    severity:  Optional[str] = Query(None),
    device_id: Optional[str] = Query(None),
    limit:     int           = Query(100)
):
    db = SessionLocal()
    try:
        query = db.query(LogRecord)
        if severity:
            query = query.filter(LogRecord.severity == severity.upper())
        if device_id:
            query = query.filter(LogRecord.device_id == device_id)
        return query.order_by(LogRecord.id.desc()).limit(limit).all()
    finally:
        db.close()

@app.get("/logs/summary", response_model=List[SummaryItem])
def get_summary():
    db = SessionLocal()
    try:
        results = (
            db.query(
                LogRecord.device_id,
                func.sum(case((LogRecord.severity == "INFO", 1), else_=0)).label("INFO"),
                func.sum(case((LogRecord.severity == "WARN", 1), else_=0)).label("WARN"),
                func.sum(case((LogRecord.severity == "ERROR", 1), else_=0)).label("ERROR"),
            )
            .group_by(LogRecord.device_id)
            .all()
        )
        return [
            SummaryItem(device_id=r.device_id, INFO=r.INFO, WARN=r.WARN, ERROR=r.ERROR)
            for r in results
        ]
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/logs/count")
def get_count(severity: Optional[str] = Query(None)):
    db = SessionLocal()
    try:
        query = db.query(LogRecord)
        if severity:
            query = query.filter(LogRecord.severity == severity.upper())
        return {"count": query.count()}
    finally:
        db.close()