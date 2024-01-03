import asyncio
from dataclasses import dataclass
import dotenv
import logging
import grpc
import time
import os
from typing import AsyncGenerator, List
from std_web_crawler.communication.grpc import crawler_coordination_pb2_grpc as grpc_services
from std_web_crawler.communication.grpc.GrpcSchedulerService import GrpcSchedulerService
from std_web_crawler.model.job import Job
from std_web_crawler.rate_limits import RateLimit, RateLimitManager
from std_web_crawler.utils import coroutine
from std_web_crawler.error import error
dotenv.load_dotenv()


# Get Config
LOG_LEVEL = os.getenv("APP_LOG_LEVEL") or error("APP_LOG_LEVEL not set!")
GRPC_LIST_ADDR = os.getenv("APP_SCHEDULER_GRPC_LIST_ADDR") or error("APP_SCHEDULER_GRPC_LIST_ADDR not set!")
GLOBAL_RPM = int(os.getenv("APP_SCHEDULER_GLOBAL_RPM") or error("APP_SCHEDULER_GLOBAL_RPM not set!"))
GLOBAL_TIME_BETWEEN_CRAWLS = 60 / GLOBAL_RPM


# Fields
_cleanup_coroutines: List[asyncio.coroutine] = []



async def start_grpc_server(service: grpc_services.SchedulerServicer):
    server = grpc.aio.server()
    grpc_services.add_SchedulerServicer_to_server(service, server)
    server.add_insecure_port(GRPC_LIST_ADDR)
    logging.info("Starting server on %s", GRPC_LIST_ADDR)
    await server.start()
    
    async def server_graceful_shutdown():
        logging.info("Starting graceful shutdown...")
        # Shuts down the server with 5 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(5)
    _cleanup_coroutines.append(server_graceful_shutdown())
    await server.wait_for_termination()



async def start_rest_server():
    pass


async def start_scheduler(service: GrpcSchedulerService, url_gen: AsyncGenerator[str, None]):
    # For each url, wait until a worker is avaliable, then send the job to the worker
    async for url in url_gen:
        await service.job_queue.put(Job(url=url))


async def main():
    async with coroutine.create_context() as ctx:
            
        #TODO create actor that loads urls from database in chuncks into memory and provides them as stream
        async def url_generator() -> AsyncGenerator[str, None]:
            while True:
                yield "https://derstandard.at"
                await asyncio.sleep(1)
        url_gen = url_generator()

        STANDARD_SERVICE = "derstandard.at"
        rate_limit_manager = RateLimitManager({
            STANDARD_SERVICE: RateLimit(rpm=60)
        })
        service = GrpcSchedulerService(rate_limit_manager)


        ctx.launch(start_grpc_server(service))
        ctx.launch(start_rest_server())
        ctx.launch(start_scheduler(service, url_gen))
        


if __name__ == "__main__":
    logging.basicConfig(level=logging.getLevelName(LOG_LEVEL))
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        logging.info("Shutting down gracefully...")
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()
