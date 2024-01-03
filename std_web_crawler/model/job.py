from dataclasses import dataclass



@dataclass(frozen=True)
class Job:
    url: str

@dataclass(frozen=True)
class JobsFinished:
    pass