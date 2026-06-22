from fastapi import FastAPI
from services.github_service import build_comment
from app.database import SessionLocal
from app.models import PipelineRun
from app.schemas import FailureRequest

from services.ai_service import analyze_log

app = FastAPI(
    title="PipelineIQ"
)

@app.get("/test-comment")
def test_comment():

    result = {
        "category": "Dependency Error",
        "root_cause": "Missing Python dependency",
        "fix": "Install pandas",
        "confidence": "95%"
    }

    return {
        "comment":
        build_comment(result)
    }

@app.get("/stats")
def get_stats():

    db = SessionLocal()

    runs = db.query(
        PipelineRun
    ).all()

    total = len(runs)

    failed = len([
        r for r in runs
        if r.status == "FAILED"
    ])

    return {
        "total_runs": total,
        "failed_runs": failed
    }


@app.get("/")
def root():

    return {
        "message": "PipelineIQ Running"
    }


@app.post("/analyze-failure")
def analyze_failure(
        data: FailureRequest):

    result = analyze_log(
        data.failure_log
    )

    db = SessionLocal()

    run = PipelineRun(
        run_id=data.run_id,
        status="FAILED",
        category=result["category"],
        confidence=result["confidence"],
        failure_log=data.failure_log,
        ai_suggestion=result["fix"]
    )

    db.add(run)
    db.commit()
    db.close()

    return result


@app.get("/pipeline-runs")
def get_pipeline_runs():

    db = SessionLocal()

    runs = db.query(
        PipelineRun
    ).all()

    db.close()

    return runs