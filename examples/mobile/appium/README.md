# Introduction
[Appium](http://appium.io/docs/en/latest/#) is an open-source project and ecosystem of related software, designed to facilitate UI automation of many app platforms, including mobile (iOS, Android, Tizen), browser (Chrome, Firefox, Safari), desktop (macOS, Windows), TV (Roku, tvOS, Android TV, Samsung), and more!

# README: Appium Test Automation with Guara Framework

## Overview
This project demonstrates how to integrate **Appium** with a local mobile application using the **Guara framework**. It contains an automated test suite implemented with **pytest**, following the **Page Transactions (PT) pattern** for better modularity and maintainability.

## Project Structure
```
project-root/
│── setup.py   # Contains setup transactions
│── home.py    # Contains home screen transactions
│── test_appium.py  # The test script
```

## Code Explanation
The `test_appium.py` script contains an automated test class using pytest. Below is a breakdown of its functionality:

### Imports
```python
from pathlib import Path
from random import randrange
from pytest import mark
from appium import webdriver
from guara.transaction import Application
from guara import it
from setup import OpenAppiumApp, CloseAppiumApp
from home import SubmitTextAppium
```
- `Path` is used to resolve file paths.
- `randrange` selects a random test input.
- `pytest` is used for structuring and running tests.
- `webdriver` from `appium` is used to interact with the mobile application.
- `Application` from `guara.transaction` manages interactions with the application.
- `it` provides assertion utilities.
- `setup` and `home` modules define test transactions.

### Test Class: `TestAppiumIntegration`
```python
@mark.skip(reason="Complex setup in CI environment")
class TestAppiumIntegration:
```
- The test class is marked with `@mark.skip`, meaning it is skipped in CI environments where setup may be complex.
- This class is responsible for testing the automation of a mobile application using Appium.

### Setup and Teardown Methods
```python
def setup_method(self, method):
    file_path = Path(__file__).resolve()
    desired_caps = {
        "platformName": "Android",
        "deviceName": "emulator-5554",
        "browserName": "Chrome",
        "app": "/absolute/path/to/sample.apk",
        "automationName": "UiAutomator2",
        "noReset": True,
        "appWaitActivity": "*",
        "goog:chromeOptions": {"args": ["--headless"]},
    }
    self.driver = webdriver.Remote(
        "http://localhost:4723/wd/hub", desired_capabilities=desired_caps
    )
    self._app = Application(self.driver)
    self._app.at(OpenAppiumApp, url=f"file:///{file_path}/sample.html")
```
- `setup_method` initializes the Appium driver with desired capabilities.
- It loads a local mobile application (`sample.apk`).
- The `appWaitActivity` wildcard (`*`) allows waiting for any activity to be ready.
- Opens a sample HTML file for testing via a `file:///` URL.

```python
def teardown_method(self, method):
    self._app.at(CloseAppiumApp)
```
- `teardown_method` ensures the application is closed after each test execution.

### Test Case: `test_local_page`
```python
def test_local_page(self):
    text = ["cheese", "appium", "test", "bla", "foo"]
    text = text[randrange(len(text))]
    self._app.at(SubmitTextAppium, text=text).asserts(it.IsEqualTo, f"It works! {text}!")
    self._app.at(SubmitTextAppium, text=text).asserts(it.IsNotEqualTo, "Any")
```
- The test randomly selects a string from a predefined list.
- It submits the text to the application and asserts that the expected response matches `"It works! {text}!"`.
- A negative assertion checks that the response is not `"Any"`.

## Notes
- Update `app` in `desired_caps` with the correct APK path before running the tests.
- Ensure the Appium server is running on `http://localhost:4723`.
- The `@mark.skip` decorator can be removed for local execution.


