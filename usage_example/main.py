import asyncio
import sys

import qasync
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

from pyqt_rest_client import login_data
from pyqt_rest_client.asyncio_integration import async_task
from usage_example import petstore_api

app: QApplication


@async_task
async def launch():
    found_pets = await petstore_api.find_pet_by_status("available").get(
        descr="Request available pets"
    )
    print(found_pets)
    app.quit()


def main():
    global app
    app = QApplication(sys.argv)
    asyncio.set_event_loop(qasync.QEventLoop(app))

    # FIXME It is a crutch to avoid login() that requires login & secret
    login_data.base_url = "https://petstore.swagger.io/v2/"

    QTimer.singleShot(0, launch)
    return app.exec_()


if __name__ == "__main__":
    exit(main())
