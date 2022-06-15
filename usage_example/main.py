import asyncio
import sys

import qasync
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, qApp

from pyqt_rest_client import async_task, login_data
from usage_example import petstore_api


@async_task
async def ask_petstore_the_available_pets_and_exit():
    found_pets = await petstore_api.find_pet_by_status("available").get(
        descr="Request available pets"
    )
    print(found_pets)
    qApp.quit()


def main():
    app = QApplication(sys.argv)
    asyncio.set_event_loop(qasync.QEventLoop(app))

    # FIXME It is a crutch to avoid login() that requires login & secret
    login_data.base_url = "https://petstore.swagger.io/v2/"

    QTimer.singleShot(0, ask_petstore_the_available_pets_and_exit)
    return app.exec_()


if __name__ == "__main__":
    exit(main())
