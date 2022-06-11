import pytest
import qasync
from pytestqt.qtbot import QtBot

import pyqt_rest_client as client
from tests.QtRequestsMock import QtRequestsMock


@pytest.fixture
def login_mock():
    client.login(
        "http://server:1234/api/v1.8/",
        "user",
        "SOME1FAKE1SECRET012345678m98u1u2u3i4ied+vew=",
    )
    return client


@pytest.fixture
def qt_requests_mock(mocker, qtbot):
    return QtRequestsMock(mocker)


@pytest.fixture
def event_loop(qapp):
    loop = qasync.QEventLoop(qapp)
    yield loop
    loop.close()


@pytest.fixture
def qtbot(qapp, request, event_loop):
    """
    To activate asyncio fot qtbot
    """
    return QtBot(request)
