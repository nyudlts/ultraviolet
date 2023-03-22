# Testing

This document contains information of how to test and write tests for the Ultraviolet application

TOC
- [Testing](#testing)
- [Introduction to Testing InvenioRDM](#introduction-to-testing-inveniordm)
- [UI Testing](#ui-testing)
- [End to End Testing](#end-to-end-testing)
  - [Prerequisites](#prerequisites)
- [Run the tests (Unit or end-to-end)](#run-the-tests-(unit-or-end-to-end))



## Introduction to Testing InvenioRDM

InvenioRDM uses [pytest framework](https://docs.pytest.org/en/6.2.x/).  
Project fixtures are provided by [flask-pytest](https://pytest-flask.readthedocs.io/en/latest/) and [pytest-invenio](https://pytest-invenio.readthedocs.io/en/latest/index.html) modules.
Ultraviolet mostly relies  on the existing InvenioRDM scaffolding for testing but several Ultraviolet specific fixtures are added and can be found in `/tests` directory.

We use the test layout recommended in pytest-invenio documentation, e.g. tests are split into three folders:
- `tests/ui/` - tests related to UI (unit testing)
- `tests/api/` - tests related to API (unit testing)
- `tests/e2e/` - tests that need both UI and API application (end-to-end tests)
- requires creating both the UI and API tests and using a special WSGI middleware to dispatch requests between both applications.

## UI Testing

Use the example in [look-feel.md](./develop/look-feel.md)

## End to End Testing

### Prerequisites

Before running E2E make sure that Selenium Client is installed and Chrome Webdriver is installed and added to you path.

[Installation instructions](https://www.selenium.dev/selenium/docs/api/py/)

## Run the tests (Unit or end-to-end)

1. Install pipenv development dependencies
  ``` sh
  pipenv install --dev
  ```
2. Make sure the application containers are running
  ``` sh
  invenio-cli services status
  ```
3. OPTIONAL: Enable end-to-end tests (disabled by default)
  ``` sh
  export E2E=yes
  ```
4. OPTIONAL: Chrome driver is used for E2E tests by default. You can switch to Firefox with the following command:
  ``` sh
  export E2E_WEBDRIVER_BROWSERS="Firefox"
  ```
5. Run the tests!
  ``` sh
  pipenv run pytest -p no:cacheprovider
  ```
6. OPTIONAL: You can (re)run specific tests by specifying the path, e.g.,
  ``` sh
  pipenv run pytest -p no:cacheprovider tests/ui
  ```
