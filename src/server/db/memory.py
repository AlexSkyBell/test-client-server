from typing import Dict, List

from server.tasks import Task

from .main import Database


class MemoryDatabase(Database):
    tasks: Dict[str, Task] = {}

    def add(self, task: Task) -> None:
        self.tasks[str(task.id)] = task

    def get(self, task_id: str) -> Task:
        return self.tasks.get(task_id)

    def get_tasks(self) -> List[Task]:
        return self.tasks.values()
