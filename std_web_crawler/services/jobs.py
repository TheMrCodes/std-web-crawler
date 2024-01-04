import asyncio
from typing import AsyncGenerator

from std_web_crawler.model.job import Job, JobResult



class JobManager:
    """
    Manages the job queue and the workers
    """

    # Fields
    _queue: asyncio.Queue[Job]


    # Constuctor
    def __init__(self, job_repository ) -> None:
        self._queue = asyncio.Queue()


    # Methods
    def create_job(self, url: str) -> Job:
        return Job(url=url)

    async def add_job(self, job: Job) -> None:
        await self._queue.put(job)

    async def add_jobs_from_url_generator(self, url_gen: AsyncGenerator[str, None]) -> None:
        async for url in url_gen:
            job = self.create_job(url)
            await self._queue.put(job)

    def get_job_queue(self) -> asyncio.Queue[Job]:
        return self._queue
    
    async def job_done(self, job: Job, result: JobResult) -> None:
        #TODO save result
        pass

