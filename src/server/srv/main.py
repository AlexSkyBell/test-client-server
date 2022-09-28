from abc import abstractmethod

from server.dispatcher import Dispatcher


class Server:
    def __init__(self, dispatcher: Dispatcher) -> None:
        self.dispatcher = dispatcher

    @abstractmethod
    async def handle(self, request) -> bytes:
        ...
