---
layout: default
title: Run Tests
parent: Develop
nav_order: 3
---
# {{ page.title }}

### Testing Scaffolding

InvenioRDM uses [pytest framework](https://docs.pytest.org/en/6.2.x/). Project fixtures are provided by [flask-pytest](https://pytest-flask.readthedocs.io/en/latest/) and [pytest-invenio](https://pytest-invenio.readthedocs.io/en/latest/index.html) modules.
Ultraviolet mostly relies  on the existing InvenioRDM scaffolding for testing but several Ultraviolet specific 
fixtures are added and can be found in `/test` directory.

### Layout 

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

### How to Run tests
A bash script which can be used to run tests is provide in the repo `./run_tests.sh`. 
The script takes path for the specific test file or test directory as a parameter. 
If path is not provided all tests will run. 
```
./run_tests.sh tests/ui
```
By default, E2E tests are skipped. If you want to do end to end testing you must set E2E environment variable to 'yes':
```
$ export E2E=yes
```
Before runnig E2E make sure that Selenium Client is installed and Chrome Webdriver is installed and added to you path.

[Installation instructions](https://www.selenium.dev/selenium/docs/api/py/)

If those requirements are not met `run_tests` script will exit with error message.
By default Chrome is used for testing. If you’d like to use Firefox, Safari or another browser you must set another environment variable:
```
$ export E2E_WEBDRIVER_BROWSERS="Firefox"
```

