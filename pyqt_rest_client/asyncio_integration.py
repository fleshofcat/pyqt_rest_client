import asyncio
from typing import Callable, List

from PyQt5.QtCore import QTimer

_release_exceptions_timers: List[QTimer] = []


def async_task(func) -> Callable:
    def sync_wrapper_around_async_func(*args, **kwargs):
        task = asyncio.create_task(func(*args, **kwargs))

        release_exceptions_timer = QTimer()
        _release_exceptions_timers.append(release_exceptions_timer)

        def check_task_exceptions_if_it_is_done():
            if task.done():
                _release_exceptions_timers.remove(release_exceptions_timer)
                release_exceptions_timer.stop()
                release_exceptions_timer.deleteLater()

                task.result()  # The release exceptions itself

        release_exceptions_timer.timeout.connect(check_task_exceptions_if_it_is_done)
        release_exceptions_timer.start(50)

    return sync_wrapper_around_async_func
