from typing import Dict, List

import pytest
from pydantic import BaseModel
from PyQt5.QtNetwork import QNetworkReply

from pyqt_rest_client.reply import ReplyGotError, Reply
from pyqt_rest_client.request import (
    cast_body_to_bytes,
    cast_reply_to_resource,
    endpoint,
)


@pytest.fixture
def dbs_endpoint():
    return endpoint(list, ["dbs"])


@pytest.mark.parametrize("operation", ["GET", "POST", "PUT", "DELETE"])
async def test_requests(qtbot, qt_requests_mock, dbs_endpoint, operation):
    request_methods = {
        "GET": (qt_requests_mock.get, dbs_endpoint.get, [""]),
        "POST": (qt_requests_mock.post, dbs_endpoint.post, [b"", ""]),
        "PUT": (qt_requests_mock.put, dbs_endpoint.put, [b"", ""]),
        "DELETE": (qt_requests_mock.delete, dbs_endpoint.delete, [""]),
    }

    request_mocker, request_method, req_args = request_methods[operation]

    # Good case
    request_mocker(dbs_endpoint.url, text="[]")
    assert await request_method(*req_args) == []

    # Bad case
    request_mocker(dbs_endpoint.url, text="", qt_err=QNetworkReply.ContentNotFoundError)
    try:
        await request_method(*req_args)
    except ReplyGotError as err:
        reply = Reply(err)
        assert not reply.ok()
        assert reply.operation() == operation


@pytest.mark.parametrize("operation", ["GET", "POST", "PUT", "DELETE"])
async def test_awaitable_requests_that_return_reply(
    qtbot, qt_requests_mock, dbs_endpoint, operation
):
    request_methods = {
        "GET": (qt_requests_mock.get, dbs_endpoint.get_and_return_bare_reply, [""]),
        "POST": (
            qt_requests_mock.post,
            dbs_endpoint.post_and_return_bare_reply,
            [b"", ""],
        ),
        "PUT": (
            qt_requests_mock.put,
            dbs_endpoint.put_and_return_bare_reply,
            [b"", ""],
        ),
        "DELETE": (
            qt_requests_mock.delete,
            dbs_endpoint.delete_and_return_bare_reply,
            [""],
        ),
    }

    request_mocker, request_method, req_args = request_methods[operation]

    # Good case
    request_mocker(dbs_endpoint.url, text="[]")
    reply = await request_method(*req_args)
    assert type(reply) is Reply
    assert reply.ok()
    assert reply.operation() == operation

    # Bad case
    request_mocker(dbs_endpoint.url, text="", qt_err=QNetworkReply.ContentNotFoundError)
    reply = await request_method(*req_args)
    assert type(reply) is Reply
    assert not reply.ok()
    assert reply.operation() == operation


@pytest.mark.parametrize("body", [bytes(b"a"), bytearray(b"a"), {"a": "a"}, ["a", "a"]])
def test__cast_body_to_bytes(body):
    casted_body = cast_body_to_bytes(body)
    assert type(casted_body) is bytes
    assert b"a" in casted_body


@pytest.mark.parametrize("body", ["a", set("a")])
def test__cast_body_to_bytes_from_unsupported_type(body):
    with pytest.raises(ValueError):
        # noinspection PyTypeChecker
        cast_body_to_bytes(body)


class _ToTestCasting(BaseModel):
    uuid: str
    count: int
    lst: list


@pytest.mark.parametrize(
    "res_type, data, expected",
    [
        (
            _ToTestCasting,
            b'{"uuid": "some_uuid", "count": 5, "lst": ["kiss", "my"]}',
            _ToTestCasting(uuid="some_uuid", count=5, lst=["kiss", "my"]),
        ),  # Pydantic dataclass
        (bytes, b"qwerty", b"qwerty"),
        (str, b"qwerty", "qwerty"),
        (list, b"[1, 2]", [1, 2]),
        (List, b"[1, 2]", [1, 2]),
        (List[int], b"[1, 2]", [1, 2]),
        (dict, b'{"q": 2}', {"q": 2}),
        (Dict, b'{"q": 2}', {"q": 2}),
        (Dict[str, int], b'{"q": 2}', {"q": 2}),
    ],
)
def test_cast_reply_to_resource(mocker, res_type, data: bytes, expected):
    mocker.patch.object(Reply, "__init__", return_value=None)
    # noinspection PyArgumentList
    reply_mock = Reply()  # type: ignore
    reply_mock.data = data

    assert expected == cast_reply_to_resource(reply_mock, res_type)


def test_value_error_at_creating_request_from_wrong_data():
    with pytest.raises(ValueError):
        Reply("Str isn't valid here. QNetworkReply, ReplyGotError only")  # type: ignore
