from __future__ import annotations

from abc import abstractclassmethod


class Request:
    @abstractclassmethod
    def parse_request(cls, body: str) -> Request:
        ...


class Response:
    ...
