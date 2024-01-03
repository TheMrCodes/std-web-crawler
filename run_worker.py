import asyncio
import dotenv
import grpc
import os
from std_web_crawler.communication.grpc import crawler_coordination_pb2_grpc as grpc_services
from std_web_crawler.communication.grpc import crawler_coordination_pb2 as grpc_messages
from std_web_crawler.crawler.derstandard import DerStandardCrawler
from std_web_crawler.error import error
dotenv.load_dotenv()



SCHEDULER_ADDRESS = os.getenv("APP_WORKER_SCHEDULER_URL") or error("APP_WORKER_SCHEDULER_URL not set!")


async def main():
    async with grpc.aio.insecure_channel(SCHEDULER_ADDRESS) as channel:
        stub = grpc_services.SchedulerStub(channel)
        response = await stub.RegisterAsWorker(request=grpc_messages.RegisterAsWorkerRequest())
        worker_id = response.id
        print(f"Registered as worker with id {worker_id}")

        async for job in stub.GetJobs(grpc_messages.GetJobsRequest(id=worker_id)):
            print(f"Received job: {job.url}")
            # Here you would typically do something with the job, like start a web crawl

if __name__ == "__main__":
    asyncio.run(main())
