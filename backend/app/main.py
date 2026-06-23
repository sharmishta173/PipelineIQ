from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.github_service import build_comment
from app.database import SessionLocal
from app.models import PipelineRun
from app.schemas import FailureRequest
from routes.metrics import (
    pipeline_runs,
    pipeline_failures
)
from services.ai_service import analyze_log
from services.github_service import (
    build_comment,
    post_commit_comment
)
from services.slack_service import send_slack_alert
from app.config import SLACK_WEBHOOK_URL


app = FastAPI(
    title="PipelineIQ"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes.health import router as health_router
app.include_router(health_router)

from routes.metrics import router as metrics_router

app.include_router(metrics_router)
from services.github_service import (
    build_comment,
    post_commit_comment
)

@app.get("/post-test-comment")
def post_test_comment():

    result = {
        "category": "Dependency Error",
        "root_cause": "Missing Python dependency",
        "fix": "Install pandas",
        "confidence": "95%"
    }

    comment = build_comment(result)

    response = post_commit_comment(
        owner="sharmishta173",
        repo="PipelineIQ",
        commit_sha="1dc3a94ac83acc4d723fac74de5f220a91989b88",
        comment_text=comment
    )

    return response

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

    runs = db.query(PipelineRun).all()

    total = len(runs)

    failed = len([
        r for r in runs
        if r.status == "FAILED"
    ])

    success_rate = (
        ((total - failed) / total) * 100
        if total > 0
        else 0
    )

    return {
        "total_runs": total,
        "failed_runs": failed,
        "success_rate": round(success_rate, 2)
    }


@app.get("/")
def root():

    return {
        "message": "PipelineIQ Running"
    }


@app.post("/analyze-failure")
def analyze_failure(
        data: FailureRequest):
    
    pipeline_runs.inc()
    pipeline_failures.inc()
    
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
        ai_suggestion=result["fix"],
        commit_sha=data.commit_sha
    )

    db.add(run)
    db.commit()
    db.close()

    send_slack_alert(
    f"""

    🚨 Pipeline Failure

    Run ID: {data.run_id}

    Category: {result['category']}

    Root Cause:
    {result['root_cause']}

    Fix:
    {result['fix']}

    Confidence:
    {result['confidence']}

    Commit:
    {data.commit_sha}
    """,
    SLACK_WEBHOOK_URL
    )

    db.close()

    return result
    
    if data.commit_sha:
     comment = build_comment(result)

     post_commit_comment(
      owner="sharmishta173",
      repo="PipelineIQ",
      commit_sha=data.commit_sha,
      comment_text=comment
    )

    return result


@app.get("/pipeline-runs")
def get_pipeline_runs():

    db = SessionLocal()

    runs = db.query(
        PipelineRun
    ).all()

    db.close()

    return runs