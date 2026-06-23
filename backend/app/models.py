from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import declarative_base
from sqlalchemy import DateTime
from datetime import datetime

created_at = Column(
    DateTime,
    default=datetime.utcnow
)

Base = declarative_base()


class PipelineRun(Base):

    __tablename__ = "pipeline_runs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    run_id = Column(String)

    status = Column(String)

    failure_log = Column(Text)

    category = Column(String)

    confidence = Column(String)

    ai_suggestion = Column(Text)