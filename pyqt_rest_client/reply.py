import json
from typing import Union, cast

from PyQt5.QtNetwork import QNetworkReply, QNetworkRequest


class ReplyGotError(Exception):
    pass


# It is a more convenient wrapper around QNetworkReply
class Reply:
    def __init__(self, reply: Union[QNetworkReply, ReplyGotError]):
        if type(reply) is QNetworkReply:
            self.reply = reply
            self.request_body: bytes = b""
            self.data: bytes = reply.readAll().data()
            self.descr: str = ""

        elif type(reply) is ReplyGotError:  # Cast back from exception
            origin: Reply = cast(Reply, reply.args[0])
            self.reply = origin.reply
            self.request_body = origin.request_body
            self.data = origin.data
            self.descr = origin.descr

        else:
            raise ValueError(
                f"reply: '{reply}' should be QNetworkReply or ReplyGotError"
            )

    def operation(self) -> str:
        return [
            "Error, operation is not valid",
            "HEAD",
            "GET",
            "PUT",
            "POST",
            "DELETE",
            "CUSTOM",
        ][self.reply.operation()]

    def url(self) -> str:
        return self.reply.url().url()

    def text(self) -> str:
        return self.data.decode("utf-8")

    def json(self) -> Union[list, dict]:
        return json.loads(self.data)

    def ok(self) -> bool:
        return self.reply.error() == QNetworkReply.NoError

    def code(self) -> int:
        return self.reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)

    def qt_error_string(self) -> str:
        return self.reply.errorString()
