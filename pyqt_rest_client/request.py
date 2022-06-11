import asyncio
import hashlib
import json
from typing import Any, Callable, Union

from pydantic import parse_obj_as
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtNetwork import QNetworkReply, QNetworkRequest

import pyqt_rest_client as client
from .reply import Reply, ReplyGotError
from .url import url


def create_authentication_header(username: str, secret: bytes, message: bytes) -> bytes:
    encoded_message = hashlib.sha256(secret + message).hexdigest()
    return bytes(f"{username}:{encoded_message}", "utf-8")


def cast_body_to_bytes(body: Union[bytes, list, dict]) -> bytes:
    if type(body) in (dict, list):
        body = json.dumps(body).encode("utf-8")
    elif type(body) not in (bytes, bytearray):
        raise ValueError(
            f"Body type: '{type(body).__name__}' must be bytes, bytearray, list or dict"
        )
    return bytes(body)


def cast_reply_to_resource(reply: Reply, res_type):
    if res_type in (bytes, bytearray):
        return res_type(reply.data)
    elif res_type is str:
        return reply.data.decode("utf-8")
    else:
        return parse_obj_as(res_type, reply.json())


class Request:
    def __init__(self, full_url: str, res_type=None, timeout_ms=5000):
        self.url = full_url
        self.res_type = res_type
        self.timeout = timeout_ms  # 1 sec == 1000 ms

    async def _request(
        self,
        request_type_dependant_operation: Callable[
            [QNetworkRequest, bytes], QNetworkReply
        ],
        body: Union[bytes, list, dict],
        descr: str,
    ) -> Union[Reply, Any]:
        reply = await self._request_and_return_bare_reply(
            request_type_dependant_operation, body, descr
        )

        if reply.ok():
            return cast_reply_to_resource(reply, self.res_type)
        else:
            raise ReplyGotError(reply)

    async def _request_and_return_bare_reply(
        self,
        request_type_dependant_operation: Callable[
            [QNetworkRequest, bytes], QNetworkReply
        ],
        body: Union[bytes, list, dict],
        descr: str,
    ):
        body = cast_body_to_bytes(body)

        request = QNetworkRequest(QUrl(self.url))
        request.setRawHeader(
            b"Authentication",
            create_authentication_header(
                client.login_data.username, client.login_data.secret, body
            ),
        )
        request.setRawHeader(b"Content-Type", b"application/json")

        qt_reply = request_type_dependant_operation(request, body)
        client.active_requests += [qt_reply]

        future = asyncio.get_event_loop().create_future()

        def _on_finished():
            reply = Reply(qt_reply)
            reply.request_body = body
            reply.descr = descr

            client.active_requests.remove(qt_reply)
            future.set_result(reply)

        # Between qt request start and finish unhandled exception will be invisible
        qt_reply.finished.connect(_on_finished)
        QTimer.singleShot(self.timeout, qt_reply.close)

        if descr:
            client.request_notifier.request_started.emit(descr)
            qt_reply.finished.connect(
                lambda: client.request_notifier.request_finished.emit(descr)
            )

        self.to_patch(qt_reply)
        return await future

    async def get(self, descr: str) -> Any:
        return await self._request(
            lambda r, _: client.network_manager.get(r), b"", descr
        )

    async def post(self, body: Union[bytes, list, dict], descr: str) -> Any:
        return await self._request(client.network_manager.post, body, descr)

    async def put(self, body: Union[bytes, list, dict], descr: str) -> Any:
        return await self._request(client.network_manager.put, body, descr)

    async def delete(self, descr: str) -> Any:
        return await self._request(
            lambda r, _: client.network_manager.deleteResource(r), b"", descr
        )

    # Requests with bare replies(not deserialized) firstly is needed for debug purposes
    # Normally these requests supposed to return deserialized pydantic dataclasses
    async def get_and_return_bare_reply(self, descr: str) -> Reply:
        return await self._request_and_return_bare_reply(
            lambda r, _: client.network_manager.get(r), b"", descr
        )

    async def post_and_return_bare_reply(
        self, body: Union[bytes, list, dict], descr: str
    ) -> Reply:
        return await self._request_and_return_bare_reply(
            client.network_manager.post, body, descr
        )

    async def put_and_return_bare_reply(
        self, body: Union[bytes, list, dict], descr: str
    ) -> Reply:
        return await self._request_and_return_bare_reply(
            client.network_manager.put, body, descr
        )

    async def delete_and_return_bare_reply(self, descr: str) -> Reply:
        return await self._request_and_return_bare_reply(
            lambda r, _: client.network_manager.deleteResource(r), b"", descr
        )

    # This method is used to implement something like `requests-mock`
    # But for qt network based requests
    def to_patch(self, qt_reply: QNetworkReply):
        pass


def endpoint(res_type, url_parts: list, args: dict = None):
    return Request(url(url_parts, args), res_type)
