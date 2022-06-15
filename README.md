# PyQt Rest Client

This package was written to make work with the REST API server async and convenient for PyQt applications.

Authentication here is calculated based on password/secret and message body.

For stable work with Qt event loop, this package uses under the hood native Qt classes for networking: `QNetworkAccessManager`, `QNetworkRequest`, `QNetworkReply`.

To use [async/await](https://iximiuz.com/en/posts/from-callback-hell-to-async-await-heaven/) pattern the client wraps Qt requests into asyncio [Future](https://docs.python.org/3/library/asyncio-future.html) objects.

## External dependencies

1. git
1. python 3.8 or later
1. poetry package manager

[Recommended way to install poetry](https://python-poetry.org/docs/#installation) and the quick one: `pip install poetry --user`

## Install

To add this library as dependency in existing poetry environment run

``` bash
poetry add git+ssh://git@github.com:fleshofcat/pyqt_rest_client.git
```

## Usage

To use the library, you need to do several steps, let's look at them using the `usage_example` in the root of the repository

1. Create your API methods set

    ``` python
    # usage_example/petstore_api.py
    from pyqt_rest_client import endpoint

    def find_pet_by_status(status: str):
        return endpoint(list, ["pet", "findByStatus"], {"status": status})
    ```

1. Make Qt and asyncio work together by setting the same event loop for them

    ``` python
    # usage_example/main.py
    import sys
    import qasync
    import asyncio

    def main():
        app = QApplication(sys.argv)
        asyncio.set_event_loop(qasync.QEventLoop(app))
        return app.exec_()
    ```

1. Make an async Qt slot with `async_task` decorator and call the API from there

    ``` python
    # usage_example/main.py
    from usage_example import petstore_api
    from pyqt_rest_client import async_task

    @async_task
    async def ask_petstore_the_available_pets():
        found_pets = await petstore_api.find_pet_by_status("available").get(
            descr="Request available pets"
        )
        print(found_pets)
    ```

1. Set the base url and call the slot

    ``` python
    # usage_example/main.py
    from pyqt_rest_client import async_task, login
    from PyQt5.QtCore import QTimer

    def main():
        ...

        # Username & secret used to calculate and set a custom Authentication header
        # For servers that allow some endpoints to work without authentication,
        # such as the petstore.swagger.io, this will be enough
        login("https://petstore.swagger.io/v2/", username="", secret="")

        QTimer.singleShot(0, ask_petstore_the_available_pets)
        return app.exec_()
    ```

As a result you will get a list of pets from petstore.swagger.io into your terminal

### Response deserialization

You can return deserialized data from requests with [pydantic](https://pydantic-docs.helpmanual.io/)

``` python
# usage_example/petstore_api.py
from typing import List, Optional
from pydantic import BaseModel
from pyqt_rest_client import endpoint

class Pet(BaseModel):
    id: int
    name: Optional[str]
    status: Optional[str]
    category: Optional[Dict]
    photoUrls: Optional[List[str]]
    tags: Optional[List[Dict]]

def find_pet_by_status(status: str):
    return endpoint(List[Pet], ["pet", "findByStatus"], {"status": status})
```

``` python
# usage_example/main.py
from usage_example import petstore_api
from usage_example.dataclasses.pet import Pet

async def ask_petstore_the_available_pets():
    found_pets = await petstore_api.find_pet_by_status("available").get(
        descr="Request available pets"
    )

    for pet in found_pets:
        assert type(pet) is Pet
        print(pet.id)
        print(pet.status)


    # Also you can use get_and_return_bare_reply() instead of get()
    found_pets_reply = await petstore_api.find_pet_by_status(
        "available"
    ).get_and_return_bare_reply(descr="Request available pets")

    for pet in found_pets_reply.json():
        assert type(pet) is dict
        print(pet["id"])
        print(pet["status"])
```

### `async_task` decorator

This function is a wrapper over async function to call it from the sync code. First of all, it is needed to connect a qt signal, which is synchronous, to an asynchronous Qt slot

``` python
from pyqt_rest_client import async_task
from usage_example import petstore_api
from PyQt5.QtCore import QTimer

@async_task
async def async_slot():
    await petstore_api.find_pet_by_status("").get("")

async def another_async_slot():
    await petstore_api.find_pet_by_status("").get("")


def sync_code():
    async_slot()
    # Or connect to it
    QTimer.singleShot(0, async_slot)

    # Also you can use `async_task` directly
    QTimer.singleShot(0, async_task(another_async_slot))
```

## [Dev notes](doc/dev_notes.md)
