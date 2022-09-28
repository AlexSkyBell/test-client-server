import asyncio
import uuid
from enum import Enum
from typing import Any, List, Optional


class TaskType(Enum):
    REVERT = "REVERT"
    SWAP = "SWAP"
    REPEAT = "REPEAT"


class TaskStatus(Enum):
    INIT = "INIT"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class Task:
    def __init__(self, type: str, args: Optional[List]) -> None:
        self.status = TaskStatus.INIT
        self.id = uuid.uuid4()
        self.type = type
        self.args = args or []
        self.result = None

    def set_status(self, status: TaskStatus) -> None:
        self.status = status

    def set_result(self, result: Any) -> None:
        self.result = result

    def serialize(self):
        return {
            "id": str(self.id),
            "type": self.type,
            "args": self.args,
            "status": self.status.value,
            "result": self.result,
        }

    async def execute(self) -> None:
        ...


class RevertTask(Task):
    async def execute(self) -> None:
        self.set_status(TaskStatus.IN_PROGRESS)
        await asyncio.sleep(2)
        self.set_status(TaskStatus.COMPLETED)
        self.set_result(self.args[0][::-1])


class SwapTask(Task):
    async def execute(self) -> None:
        # TODO: self.args[0] must be iterable
        self.set_status(TaskStatus.IN_PROGRESS)
        await asyncio.sleep(5)
        res = []
        for first, second in zip(*[iter(self.args[0])] * 2):
            res.extend([second, first])
        if len(self.args[0]) % 2 == 1:
            res.append(self.args[0][-1])
        self.set_status(TaskStatus.COMPLETED)
        self.set_result("".join(res))


class RepeatTask(Task):
    async def execute(self) -> None:
        self.set_status(TaskStatus.IN_PROGRESS)
        await asyncio.sleep(7)
        res = []
        for index, letter in enumerate(self.args[0]):
            res.extend([letter] * (index + 1))
        self.set_status(TaskStatus.COMPLETED)
        self.set_result("".join(res))


class TaskFactory:
    @classmethod
    def create_task(self, task_type: str, args: Optional[List] = None) -> Task:
        return {
            TaskType.REVERT.value: RevertTask,
            TaskType.SWAP.value: SwapTask,
            TaskType.REPEAT.value: RepeatTask,
        }.get(task_type)(task_type, args)
