import asyncio
from typing import List, Optional

from .task import Task


# TODO: must be singleton
class TasksPool:
    def __init__(self) -> None:
        self.queue = asyncio.Queue()

    def add(self, task: Task) -> None:
        self.queue.put_nowait(task)

    async def get_ordered_task(self) -> Optional[Task]:
        return await self.queue.get()
