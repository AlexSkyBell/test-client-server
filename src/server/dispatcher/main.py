from abc import abstractmethod

from server.app.req_res import Request, Response
from server.control import Control


class Dispatcher:
    def __init__(self, task_view: Control) -> None:
        self.task_view = task_view
        self.routers = {}
        self.build_routers()

    @abstractmethod
    def build_routers(self):
        ...

    @abstractmethod
    async def dispatch(self, request: Request) -> Response:
        ...
