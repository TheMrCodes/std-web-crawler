from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from std_web_crawler.db.base import BaseModel


class JobStatus:
    CREATED = "created"
    STARTED = "started"
    FINISHED = "finished"


class Job(BaseModel):
    __incomplete_tablename__ = "jobs"

    id: Mapped[int]                             = mapped_column(Integer, primary_key=True, autoincrement=True)
    url: Mapped[str]                            = mapped_column(String(2000), nullable=False)
    status: Mapped[str]                         = mapped_column(String(255), nullable=False)
    result: Mapped[Optional[str]]               = mapped_column(String(255), nullable=True, default=None)
    created_at: Mapped[datetime]                = mapped_column(DateTime, nullable=False)
    started_at: Mapped[Optional[datetime]]      = mapped_column(DateTime, nullable=True, default=None)
    finished_at: Mapped[Optional[datetime]]     = mapped_column(DateTime, nullable=True, default=None)

    def __repr__(self) -> str:
        return f"<Job(id={self.id}, url={self.url}, status={self.status}, result={self.result}, created_at={self.created_at}, started_at={self.started_at}, finished_at={self.finished_at})>"
