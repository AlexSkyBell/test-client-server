from abc import abstractmethod
from typing import Dict, List, Optional

from server.db import Database
from server.tasks import Task, TasksPool


class Control:
    def __init__(self, pool: TasksPool, db: Database) -> None:
        self.pool = pool
        self.db = db

    @abstractmethod
    def add_task(self, task: Task) -> None:
        ...

    @abstractmethod
    def get_task(self, task_id: str) -> Task:
        ...

    @abstractmethod
    def get_tasks(self) -> List[Task]:
        ...

    @abstractmethod
    def create_task(self, type: str, args: Optional[List] = None) -> None:
        ...
