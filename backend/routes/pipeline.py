from fastapi import APIRouter

from app.services.azure_service import trigger_pipeline
from app.database import SessionLocal
from app.models import PipelineRun



router = APIRouter()

@router.post("/trigger")
def trigger():

    result = trigger_pipeline()

    return {
        "message": "Pipeline triggered",
        "result": result
    }

@router.get("/pipeline-runs")
def get_pipeline_runs():

    db = SessionLocal()

    runs = db.query(
        PipelineRun
    ).all()

    return runs