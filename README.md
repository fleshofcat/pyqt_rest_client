# PyQt Rest Client

This package was written to make work with the REST API server async and convenient for PyQt applications.

Authentication here is calculated based on password/secret and message body.

For stable work with qt event loop, this package uses under the hood native qt classes for networking: `QNetworkAccessManager`, `QNetworkRequest`, `QNetworkReply`.

To use [async/await](https://iximiuz.com/en/posts/from-callback-hell-to-async-await-heaven/) pattern the client wraps qt requests into python [Future](https://docs.python.org/3/library/asyncio-future.html) objects.

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
    from pyqt_rest_client.request import endpoint

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

1. Set base url and call the slot

    ``` python
    # usage_example/main.py
    def main():
        ...

        # Username & secret will be used to calculate and set Authentication header
        # For servers that allow some endpoints to work without authentication,
        # such as the petstore.swagger.io, this will be enough
        login("https://petstore.swagger.io/v2/", username="", secret="")

        QTimer.singleShot(0, ask_petstore_the_available_pets)
        return app.exec_()
    ```

In result you will get a list of pets from petstore.swagger.io into your terminal

## Install the development environment

``` bash
git clone git@github.com:fleshofcat/pyqt_rest_client.git
cd pyqt_rest_client
poetry install

# It is automated code checkers (black, flake8...)
poetry run pre-commit install -t=pre-commit -t=pre-push
```

### Run tests

``` bash
# poetry run <command> == run <command> inside virtual environment
poetry run pytest tests/

# To see coverage statistics
poetry run pytest --cov-config=.coveragerc --cov=./ --cov-report term-missing tests/
```


