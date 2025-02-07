# Introduction

[RPA for Python's](https://github.com/tebelorg/RPA-Python) simple and powerful API makes robotic process automation fun! You can use it to quickly automate away repetitive time-consuming tasks on websites, desktop applications, or the command line.

# README: RPA Test Automation with Guara Framework

## Overview
This project demonstrates the integration of **RPA for Python** with a local desktop application using the **Guara framework**. It contains an automated test suite implemented with **pytest**, following the **Page Transactions (PT) pattern** for better maintainability and reusability of test automation.

## Project Structure
```
project-root/
│── examples/
│   ├── linux_desktop/
│   │   ├── rpa_python/
│   │   │   ├── setup.py   # Contains setup transactions
│   │   │   ├── home.py    # Contains home screen transactions
│── test_rpa.py  # The test script
```

## Code Explanation
The `test_rpa.py` script contains an automated test class using pytest. Below is a breakdown of its functionality:

### Imports
```python
import rpa as r
import pytest
from guara.transaction import Application
from guara import it
from examples.linux_desktop.rpa_python import setup
from examples.linux_desktop.rpa_python import home
```
- `rpa` is the Robotic Process Automation library.
- `pytest` is used for structuring and running tests.
- `Application` from `guara.transaction` helps manage application interactions.
- `it` provides assertion utilities.
- `setup` and `home` modules define test transactions.

### Test Class: `TestRPAIntegration`
```python
@pytest.mark.skip(reason="Complex setup in CI environment")
class TestRPAIntegration:
```
- The test class is marked with `@pytest.mark.skip`, meaning it is skipped in CI environments where setup may be complex.
- This class is responsible for testing the automation of a desktop application using RPA.

### Setup and Teardown Methods
```python
def setup_method(self, method):
    self._app = Application(r)
    self._app.at(setup.OpenApplication, app_path="path/to/application.exe")
```
- `setup_method` initializes the `Application` instance with RPA and opens the application before each test.
- The `app_path` should be replaced with the actual path of the application being tested.

```python
def teardown_method(self, method):
    self._app.at(setup.CloseApplication)
```
- `teardown_method` ensures the application is closed after each test execution.

### Test Case: `test_submit_text`
```python
def test_submit_text(self):
    text = "Hello, RPA for Python!"
    self._app.at(home.SubmitTextRPA, text=text).asserts(it.IsEqualTo, text)
```
- The test inputs the text **"Hello, RPA for Python!"** into the application and verifies the expected output using assertions.

## Notes
- This implementation follows the **Page Transactions (PT) pattern**, making automation code modular and reusable.
- Update `app_path` to the actual executable path before running the tests.
- The `@pytest.mark.skip` decorator can be removed if running in a local setup.
