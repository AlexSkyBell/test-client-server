import logging
from datetime import datetime

from server.tasks import TasksPool


class TasksExecutor:
    def __init__(self, pool: TasksPool) -> None:
        self.pool = pool

    async def run(self) -> None:
        logging.info("Task executor ready")
        while True:
            task = await self.pool.get_ordered_task()
            now = datetime.now()
            logging.info(f"run task {task.id} type {task.type} args {task.args}")
            await task.execute()
            logging.info(
                f"task {task.id} completed in {datetime.now() - now} result {task.result}"
            )
