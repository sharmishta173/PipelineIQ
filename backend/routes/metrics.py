from fastapi import APIRouter
from prometheus_client import Counter
from prometheus_client import generate_latest
from fastapi.responses import Response

router = APIRouter()

pipeline_runs = Counter(
    "pipeline_runs_total",
    "Total pipeline runs"
)

pipeline_failures = Counter(
    "pipeline_failures_total",
    "Total pipeline failures"
)

@router.get("/metrics")
def metrics():

    return Response(
        generate_latest(),
        media_type="text/plain"
    )