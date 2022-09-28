import asyncio
import logging

from server.srv import Server


class App:
    def __init__(self, server: Server) -> None:
        self.server = server

    async def start_server(self, host, port) -> None:
        logging.info(f"Server ready on {host=} {port=}")
        server = await asyncio.start_server(self.handle_client, host, port)
        await server.serve_forever()

    async def handle_client(self, reader, writer) -> None:
        request = await self.read_request(reader)
        response = await self.server.handle(request)
        writer.write(response)
        await writer.drain()

    async def read_request(self, reader) -> str:
        request = b""
        chunk_size = 1024
        while not reader.at_eof():
            request += await reader.read(chunk_size)
            reader.feed_eof()
        return request.decode()
