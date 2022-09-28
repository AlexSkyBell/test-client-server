import logging
from typing import List, Optional

from server.tasks import Task, TaskFactory

from .main import Control


class TasksControl(Control):
    def add_task(self, task: Task) -> None:
        self.db.add(task)
        self.pool.add(task)

    def get_task(self, task_id: str) -> Task:
        return self.db.get(task_id)

    def get_tasks(self) -> List[Task]:
        return self.db.get_tasks()

    def create_task(self, type: str, args: Optional[List] = None) -> str:
        task = TaskFactory.create_task(type, args)
        self.add_task(task)
        logging.info(f"task created {task.id} type {task.type} args {task.args}")
        return str(task.id)
