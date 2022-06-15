# Dev notes

## Install the development environment

``` bash
git clone git@github.com:fleshofcat/pyqt_rest_client.git
cd pyqt_rest_client
poetry install

# It is automated code checkers setup (black, flake8...)
poetry run pre-commit install -t=pre-commit -t=pre-push
```

## Run tests

``` bash
# poetry run <command> == run <command> inside virtual environment
poetry run pytest tests/

# To see coverage statistics
poetry run pytest --cov-config=.coveragerc --cov=./ --cov-report term-missing tests/
```
