from pydantic import BaseModel

class PipelineRunResponse(BaseModel):

    run_id: str
    status: str
    ai_suggestion: str | None

    class Config:
        from_attributes = True


class FailureRequest(BaseModel):

    run_id: str
    failure_log: str