from abc import abstractmethod
from typing import List

from server.tasks import Task


class Database:
    @abstractmethod
    def add(self, task: Task) -> None:
        ...

    @abstractmethod
    def get(self, task_id: str) -> Task:
        ...

    @abstractmethod
    def get_tasks(self) -> List[Task]:
        ...
