import pyqt_rest_client as client
from pyqt_rest_client import endpoint


def some_endpoint():
    return endpoint(str, ["some", "endpoint"])


async def test_request_started_finished_signals(login_mock, qtbot, qt_requests_mock):
    qt_requests_mock.get("http://server:1234/api/v1.8/some/endpoint/")
    request_notifier = client.request_notifier
    request_description = "some description"

    with qtbot.wait_signal(request_notifier.request_finished) as request_finished:
        with qtbot.wait_signal(request_notifier.request_started) as request_started:
            await some_endpoint().get(descr=request_description)

    assert request_finished.args == request_started.args == [request_description]


async def test_requests_without_description_are_not_logged(
    login_mock, qtbot, qt_requests_mock
):
    qt_requests_mock.get("http://server:1234/api/v1.8/some/endpoint/")
    request_notifier = client.request_notifier

    with qtbot.assertNotEmitted(request_notifier.request_finished):
        with qtbot.assertNotEmitted(request_notifier.request_started):
            await some_endpoint().get(descr="")
