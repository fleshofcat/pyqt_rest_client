import base64
from typing import List

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply

from pyqt_rest_client.asyncio_integration import async_task  # noqa


class Login:
    base_url: str
    username: str
    secret: bytes

    def __init__(self, base_url: str, username: str, secret: str):
        self.base_url = base_url
        self.username = username
        self.secret = base64.b64decode(secret)


login_data = Login("", "", "")


def login(base_url: str, username: str, secret: str):
    global login_data
    login_data = Login(base_url, username, secret)


class _RequestNotifier(QObject):
    # The str there is a description that programmer can attach to the request
    request_started = pyqtSignal(str)
    request_finished = pyqtSignal(str)


# This is made for client apps to have the ability to manually log requests
request_notifier = _RequestNotifier()


network_manager = QNetworkAccessManager()
active_requests: List[QNetworkReply] = []
