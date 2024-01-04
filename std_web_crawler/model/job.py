from dataclasses import dataclass
from datetime import datetime



@dataclass(frozen=True)
class Job:
    url: str

@dataclass(frozen=True)
class JobResult:
    title: str
    html_content: str
    finished_at: datetime

@dataclass(frozen=True)
class JobsFinished:
    pass