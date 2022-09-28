import asyncio
import logging
import time

from server.app import App, TasksExecutor
from server.control import TasksControl
from server.db.memory import MemoryDatabase
from server.dispatcher import TasksDispatcher
from server.logger import setup_logger
from server.srv import WebServer
from server.tasks import TasksPool


async def run_server(pool: TasksPool):
    host = "127.0.0.1"
    port = 8080
    db = MemoryDatabase()
    control = TasksControl(pool, db)
    dispatcher = TasksDispatcher(control)
    webserver = WebServer(dispatcher)
    app = App(webserver)
    await app.start_server(host, port)


async def run_worker(pool: TasksPool):
    executor = TasksExecutor(pool)
    await executor.run()


def main():
    loop = asyncio.get_event_loop()
    try:
        pool = TasksPool()
        loop.create_task(run_server(pool))
        loop.create_task(run_worker(pool))
        loop.run_forever()
    except Exception as exc:
        print(exc)


if __name__ == "__main__":
    setup_logger()
    main()
