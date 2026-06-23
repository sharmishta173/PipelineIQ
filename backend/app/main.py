from fastapi import FastAPI
from services.github_service import build_comment
from app.database import SessionLocal
from app.models import PipelineRun
from app.schemas import FailureRequest

from services.ai_service import analyze_log

app = FastAPI(
    title="PipelineIQ"
)
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