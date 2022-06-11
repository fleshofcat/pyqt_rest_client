import json

import pytest
from PyQt5.QtCore import QUrl, QByteArray
from PyQt5.QtNetwork import QNetworkRequest, QNetworkReply

from pyqt_rest_client.reply import Reply, ReplyGotError
import pyqt_rest_client as client


def qt_reply() -> QNetworkReply:
    return client.network_manager.get(QNetworkRequest(QUrl()))


@pytest.mark.parametrize("reply_source", [qt_reply(), ReplyGotError(Reply(qt_reply()))])
def test_init(reply_source):
    reply = Reply(reply_source)
    assert reply.reply
    assert reply.request_body == b""
    assert reply.data == b""
    assert reply.descr == ""


def test_bad_init():
    with pytest.raises(ValueError):
        # noinspection PyTypeChecker
        Reply("bad data source")


@pytest.mark.parametrize(
    "qt_reply_operation_index, expected",
    [(0, "Error, operation is not valid"), (2, "GET"), (6, "CUSTOM")],
)
def test_operation(mocker, qt_reply_operation_index, expected):
    mocked_qt_reply = qt_reply()
    mocker.patch.object(
        mocked_qt_reply, "operation", return_value=qt_reply_operation_index
    )

    reply = Reply(mocked_qt_reply)
    assert reply.operation() == expected


def test_methods_that_depends_on_qt_reply(mocker):
    mocked_qt_reply = qt_reply()
    mocker.patch.object(
        mocked_qt_reply, "readAll", return_value=QByteArray(b'{"some": "data"}')
    )
    reply = Reply(mocked_qt_reply)

    assert reply.data == b'{"some": "data"}'
    assert reply.text() == '{"some": "data"}'
    assert reply.json() == {"some": "data"}

    mocker.patch.object(mocked_qt_reply, "error", return_value=QNetworkReply.NoError)
    assert reply.ok()

    mocker.patch.object(mocked_qt_reply, "operation", return_value=2)
    assert reply.operation() == "GET"

    mocker.patch.object(mocked_qt_reply, "url", return_value=QUrl("http://some:1234"))
    assert reply.url() == "http://some:1234"

    mocker.patch.object(mocked_qt_reply, "attribute", return_value=200)
    assert reply.code() == 200

    mocker.patch.object(mocked_qt_reply, "errorString", return_value="Some error")
    assert reply.qt_error_string() == "Some error"
