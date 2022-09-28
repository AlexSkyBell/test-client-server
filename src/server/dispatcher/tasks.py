import json
import re
from http import HTTPStatus

from server.srv.req_res import WebRequest, WebResponse

from .main import Dispatcher


class TasksDispatcher(Dispatcher):
    def build_routers(self):
        self.routers = {
            re.compile("/task/(?P<task_id>[\w-]+)/result"): self.task_result_handler,
            re.compile("/task/(?P<task_id>[\w-]+)"): self.task_handler,
            re.compile("/task/"): self.tasks_handler,
            re.compile("/"): self.front_handler,
        }

    async def dispatch(self, request: WebRequest) -> WebResponse:
        for prog, handler in self.routers.items():
            if result := prog.match(request.path):
                return handler(request, **result.groupdict())

        return WebResponse("Not found", HTTPStatus.NOT_FOUND)

    def front_handler(self, request: WebRequest, *args, **kwargs) -> WebResponse:
        return WebResponse("front page")

    def task_result_handler(
        self, request: WebRequest, task_id, *args, **kwargs
    ) -> WebResponse:
        if task := self.task_view.get_task(task_id):
            return WebResponse(json.dumps({"result": task.result}))
        return WebResponse("Not found", HTTPStatus.NOT_FOUND)

    def task_handler(
        self, request: WebRequest, task_id, *args, **kwargs
    ) -> WebResponse:
        if task := self.task_view.get_task(task_id):
            return WebResponse(json.dumps(task.serialize()))
        return WebResponse("Not found", HTTPStatus.NOT_FOUND)

    def tasks_handler(self, request: WebRequest, *args, **kwargs) -> WebResponse:
        if request.method.lower() == "post":
            task_id = self.task_view.create_task(**request.json)
            return WebResponse(json.dumps({"task_id": task_id}))
        return WebResponse(
            json.dumps({"data": [t.serialize() for t in self.task_view.get_tasks()]})
        )
