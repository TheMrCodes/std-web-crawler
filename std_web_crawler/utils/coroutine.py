import asyncio
from typing import Coroutine, List



class CoroutineContext:

    # Fields
    loop: asyncio.AbstractEventLoop
    _context: List[asyncio.Task]


    def __init__(self):
        self._context = []

    
    async def __aenter__(self):
        self.loop = asyncio.get_running_loop()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        If exit is reached without an exception, await all tasks in the context.
        If an exception is raised, cancel all tasks in the context.
        """
        if exc_type is None:
            return [await task for task in self._context]
        else:
            [task.cancel() for task in self._context]


    def launch(self, coroutine: Coroutine):
        task = self.loop.create_task(coroutine)
        self._context.append(task)
        return task
    
    async def withContext(self, coroutine: Coroutine):
        return await self.launch(coroutine)
    
    async def withTimeout(self, coroutine: Coroutine, timeout: int):
        return await asyncio.wait_for(self.launch(coroutine), timeout=timeout, loop=self.loop)

    def runBlocking(self, coroutine: Coroutine):
        return self.loop.run_until_complete(coroutine)


def create_context() -> CoroutineContext:
    return CoroutineContext()
