from server.srv import Server
from server.srv.req_res import WebRequest, WebResponse


class WebServer(Server):
    def build_response(self, response: WebResponse) -> bytes:
        return f"""HTTP/1.1 {response.status}
Content-Type: application/json; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: {len(response.content)}
Accept-Ranges: bytes
Connection: closed

{response.content}""".encode(
            "utf-8"
        )

    async def handle(self, request: str) -> bytes:
        req = WebRequest.parse_request(request)
        response = await self.dispatcher.dispatch(req)
        return self.build_response(response)
