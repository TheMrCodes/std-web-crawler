import asyncio
import logging
import grpc
import os

from typing import AsyncGenerator, AsyncIterator, List, Union
from std_web_crawler.communication.grpc import crawler_coordination_pb2_grpc as grpc_services
from std_web_crawler.communication.grpc import crawler_coordination_pb2 as grpc_messages
from std_web_crawler.model.job import Job, JobsFinished
from std_web_crawler.services.rate_limits import RateLimitManager
from std_web_crawler.error import ExitCode, error



WORKER_TIMEOUT = float(os.getenv("APP_SCHEDULER_WORKER_TIMEOUT", 30) or error("APP_SCHEDULER_WORKER_TIMEOUT not set!"))




class GrpcSchedulerService(grpc_services.SchedulerServicer):

    # Fields
    #job_queue: asyncio.Queue[Job]
    _rate_limit_manager: RateLimitManager
    _worker_id_counter: int = 0
    _avaliable_workers: List[str]


    # Constructor
    def __init__(self, rate_limit_manager: RateLimitManager, buffer_size: int = 1000):
        self._rate_limit_manager = rate_limit_manager
        self.job_queue = asyncio.Queue(maxsize=buffer_size)
        self._worker_id_counter = 0
        self._avaliable_workers = []


    def RegisterAsWorker(self, request: grpc_messages.RegisterAsWorkerReply, context: grpc.ServicerContext) -> grpc_messages.RegisterAsWorkerReply:
        ret_id = self._worker_id_counter
        self._worker_id_counter += 1
        return grpc_messages.RegisterAsWorkerReply(id=str(ret_id))
    
    async def GetJobs(self, request_iterator: AsyncIterator[grpc_messages.GetJobsRequest], context: grpc.ServicerContext) -> AsyncGenerator[grpc_messages.GetJobsReply, bool]:
        try:
            request = await request_iterator.__anext__()

            # Register the worker as avaliable
            worker_id = str(request.id)
            self._avaliable_workers.append(worker_id)

            while True:
                # Wait for new job
                job = await self.job_queue.get()

                # Wait until the url is avaliable
                retries = self._rate_limit_manager.get_retries(job.url)
                await self._rate_limit_manager.wait_for_access(job.url)

                # return new job
                success = yield grpc_messages.GetJobsReply(
                    id=worker_id,
                    url=job.url,
                    retries=retries,
                )
                print(success)

            
        finally:
            # Unregister the worker as avaliable
            self._avaliable_workers.remove(worker_id)
