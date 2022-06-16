import asyncio
import sys

import qasync
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, qApp

from pyqt_rest_client import async_task, login
from pyqt_rest_client.reply import Reply, ReplyGotError
from usage_example import petstore_api


@async_task
async def ask_petstore_the_available_pets_and_exit():
    try:
        found_pets = await petstore_api.find_pet_by_status("available").get(
            descr="Request available pets"
        )
        print(found_pets)
    except ReplyGotError as e:
        reply = Reply(e)

        print(
            f"The request failed with {reply.http_code()=} "
            f"and {reply.qt_error_string()=}"
        )

    finally:
        qApp.quit()


def main():
    app = QApplication(sys.argv)
    asyncio.set_event_loop(qasync.QEventLoop(app))

    # Username & secret will be used to calculate and set Authentication header
    # For servers that allow some endpoints to work without authentication,
    # such as the petstore.swagger.io, this will be enough
    login("https://petstore.swagger.io/v2/", username="", secret="")

    QTimer.singleShot(0, ask_petstore_the_available_pets_and_exit)
    return app.exec_()


if __name__ == "__main__":
    exit(main())
