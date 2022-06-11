from PyQt5.QtCore import QByteArray, QTimer
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply

from pyqt_rest_client.request import Request


class QtRequestsMock:
    def __init__(self, mocker):
        self.registered_urls = {}
        self.mocker = mocker
        self.mocker.patch.object(
            Request, "to_patch", side_effect=self._patch_registered_replies
        )

    def _patch_registered_replies(self, reply: QNetworkReply):
        try:
            url = reply.url().url()
            if url[-1] != "/":
                url += "/"

            text, status_code, qt_err = self.registered_urls[(url, reply.operation())]
            self.mocker.patch.object(reply, "error", return_value=qt_err)
            self.mocker.patch.object(reply, "attribute", return_value=status_code)
            self.mocker.patch.object(
                reply, "readAll", return_value=QByteArray(text.encode("utf-8"))
            )
            QTimer.singleShot(1, reply.close)
        except KeyError:
            pass

    def _register_mock(
        self,
        operation,
        url: str,
        text: str,
        status_code: int,
        qt_err: QNetworkReply.NetworkError,
    ):
        if url[-1] != "/":
            url += "/"

        self.registered_urls[(url, operation)] = text, status_code, qt_err

    def get(
        self,
        url: str,
        text: str = "",
        status_code: int = 200,
        qt_err: QNetworkReply.NetworkError = QNetworkReply.NoError,
    ):
        self._register_mock(
            QNetworkAccessManager.GetOperation, url, text, status_code, qt_err
        )

    def post(
        self,
        url: str,
        text: str = "",
        status_code: int = 200,
        qt_err: QNetworkReply.NetworkError = QNetworkReply.NoError,
    ):
        self._register_mock(
            QNetworkAccessManager.PostOperation, url, text, status_code, qt_err
        )

    def put(
        self,
        url: str,
        text: str = "",
        status_code: int = 200,
        qt_err: QNetworkReply.NetworkError = QNetworkReply.NoError,
    ):
        self._register_mock(
            QNetworkAccessManager.PutOperation, url, text, status_code, qt_err
        )

    def delete(
        self,
        url: str,
        text: str = "",
        status_code: int = 200,
        qt_err: QNetworkReply.NetworkError = QNetworkReply.NoError,
    ):
        self._register_mock(
            QNetworkAccessManager.DeleteOperation, url, text, status_code, qt_err
        )
