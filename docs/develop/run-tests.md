---
layout: default
title: Run Tests
parent: Develop
nav_order: 3
---
# {{ page.title }}

## Testing Scaffolding

InvenioRDM uses [pytest framework](https://docs.pytest.org/en/6.2.x/). Project fixtures are provided by [flask-pytest](https://pytest-flask.readthedocs.io/en/latest/) and [pytest-invenio](https://pytest-invenio.readthedocs.io/en/latest/index.html) modules.
Ultraviolet mostly relies  on the existing InvenioRDM scaffolding for testing but several Ultraviolet specific
fixtures are added and can be found in `/test` directory.

## Layout

We use test layout recommended in pytest-invenio documentation, e.g. tests are splited into three folders:
```
tests/ui/
tests/api/
tests/e2e/
```
Each subfolder holds tests related to a specific application (UI or API).
The e2e folder holds tests that need both UI and API application (which is typically the case for end-to-end tests)
The E2E tests works by creating both the UI and API applications and using a special WSGI middleware
to dispatch requests between both applications.

## Prerequisites

Before running E2E make sure that Selenium Client is installed and Chrome Webdriver is installed and added to you path.

[Installation instructions](https://www.selenium.dev/selenium/docs/api/py/)

## Instructions

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
