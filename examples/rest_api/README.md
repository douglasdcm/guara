# README: REST API Test Automation with Guara Framework

## Overview
This project demonstrates how to test a **REST API** using the **Guara framework**. The test suite is implemented using **pytest** and follows the **Page Transactions (PT) pattern** to enhance modularity and maintainability.

## Project Structure
```
project-root/
│── examples/
│   ├── rest_api/
│   │   ├── echo_api.py   # Contains API transactions
│── test_rest_api.py  # The test script
```

## Code Explanation
The `test_rest_api.py` script contains an automated test class using pytest. Below is a breakdown of its functionality:

### Imports
```python
from examples.rest_api import echo_api
from guara.transaction import Application
from guara import it
```
- `echo_api` contains the API transaction definitions.
- `Application` from `guara.transaction` manages API interactions.
- `it` provides assertion utilities.

### Test Class: `TestEchoApi`
```python
class TestEchoApi:
```
- This class is responsible for testing the **echo API** using Guara’s transaction-based approach.

### Setup Method
```python
def setup_method(self, method):
    self._app = Application(None)
```
- `setup_method` initializes an `Application` instance. Since this is a REST API test, no UI driver is required, so `None` is passed.

### Test Case: `test_get_asserts_has_key_value`
```python
def test_get_asserts_has_key_value(self):
    path = {"any": "any", "foo1": "bar1s"}
    expected = {"foo1": "bar1s"}
    self._app.at(echo_api.Get, path=path).asserts(it.HasKeyValue, expected)
```
- Sends a **GET** request with a query parameter `path`.
- Asserts that the response contains the expected key-value pair.

### Test Case: `test_get`
```python
def test_get(self):
    expected = {"foo1": "bar1", "foo2": "bar2"}
    self._app.at(echo_api.Get, path=expected).asserts(it.IsEqualTo, expected)
```
- Sends a **GET** request with query parameters.
- Asserts that the entire response matches the expected data.

### Test Case: `test_post`
```python
def test_post(self):
    expected = "This is expected to be sent back as part of response body."
    self._app.at(echo_api.Post, data=expected).asserts(it.IsEqualTo, expected)
```
- Sends a **POST** request with a body payload.
- Asserts that the response body matches the expected data.

## Notes
- The **Guara framework** is used to structure API tests using transactions, making it easy to reuse test logic.
- The API being tested is an **echo API**, meaning it simply returns the sent request data.

