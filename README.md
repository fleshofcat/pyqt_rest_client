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

## TODO Describe usage

## Install for development

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


