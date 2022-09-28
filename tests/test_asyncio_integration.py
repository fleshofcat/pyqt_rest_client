from asyncio import sleep

from PyQt5.QtCore import QTimer

from pyqt_rest_client import asyncio_integration

async_action_completed = False


@asyncio_integration.async_task
async def async_function_that_we_run_as_synch():
    await sleep(0.5)

    global async_action_completed
    async_action_completed = True


def test_async_task_decorator(qtbot):
    async_function_that_we_run_as_synch()
    qtbot.wait_until(lambda: async_action_completed)


def test_connect_async_task_decorator_as_a_slot(qtbot):
    QTimer.singleShot(1, async_function_that_we_run_as_synch)
    qtbot.wait_until(
        lambda: async_action_completed
        and not asyncio_integration._release_exceptions_timers
    )
