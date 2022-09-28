from __future__ import annotations

import json
from http import HTTPStatus

from server.app.req_res import Request, Response


class WebRequest(Request):
    def __init__(self, method: int, path: str, body: str) -> None:
        self.method = method
        self.path = path
        self.body = body
        if method.lower() == "post":
            # TODO: add parse by content-type
            self.json = json.loads(body)

    @classmethod
    def parse_request(cls, body: str) -> WebRequest:
        headers, body = body.split("\r\n\r\n")
        http_lines = headers.split("\r\n")
        method, path, _ = http_lines[0].split(" ")

        return cls(method, path, body)


class WebResponse(Response):
    def __init__(self, content: str, status: str = HTTPStatus.OK) -> None:
        self.content = content
        self.status = status
