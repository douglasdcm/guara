# Introduction

Even being possible to use this framework with unit tests it is overkill.

# README: Test Automation with Guara Framework

## Overview
This project demonstrates how to test **asynchronous transactions** on a **To-Do List**, **calculator operations**, and **To-Do List operations** using the **Guara framework**. The test suites are implemented using **pytest-asyncio**, **unittest-based frameworks**, and **Guara's transaction-based approach**, following the **Page Transactions (PT) pattern** for improved modularity and maintainability.

## Project Structure
```
project-root/
│── examples/
│   ├── unit_test/
│   │   ├── async_todo_list/
│   │   │   ├── async_todo.py    # Async To-Do List implementation
│   │   │   ├── operations.py    # Transaction operations (Add, Remove, ListTasks)
│   │   ├── calculator/
│   │   │   ├── calculator.py    # Calculator implementation
│   │   │   ├── operations.py    # Calculator operations (Add, Subtract)
│   │   ├── todo_list/
│   │   │   ├── todo.py          # To-Do List implementation
│   │   │   ├── operations.py    # To-Do List operations (Add, Remove, ListTasks, PrintDict, GetBy)
│── test_async_todo.py  # The test script for Async To-Do List
│── test_calculator.py   # The test script for Calculator
│── test_todo.py         # The test script for To-Do List
```

## Async To-Do List Test Automation
### Code Explanation
The `test_async_todo.py` script contains an automated test class using `pytest-asyncio`. Below is a breakdown of its functionality:

### Imports
```python
from examples.unit_test.async_todo_list.async_todo import AsyncToDo
from guara.asynchronous.transaction import Application
from pytest_asyncio import fixture
from typing import List, Coroutine, Any
from examples.unit_test.async_todo_list.operations import Add, Remove, ListTasks
from guara.asynchronous.it import IsEqualTo, IsNotEqualTo, Contains, DoesNotContain
from pytest import mark
```

### Test Class: `TestAsyncToDo`
```python
class TestAsyncToDo:
```
- This class is responsible for testing the **asynchronous To-Do List** transactions.

### Setup Method
```python
@fixture(loop_scope="function")
async def setup_test(self) -> None:
    self._todo: Application = Application(AsyncToDo())
```

---

## Calculator Test Automation
### Code Explanation
The `test_calculator.py` script contains automated test cases for a simple calculator application. Below is a breakdown:

### Imports
```python
from random import randrange
from unittest import TestCase
from testify import TestCase as TTC, setup
from examples.unit_test.calculator.calculator import Calculator
from examples.unit_test.calculator import operations
from guara.transaction import Application
from guara import it
```

### Test Class: `TestCalculator`
```python
class TestCalculator:
    def setup_method(self, method):
        self._calculator = Application(Calculator())
```
- Initializes a `Calculator` application instance using Guara's transaction-based approach.

---

## To-Do List Test Automation
### Code Explanation
The `test_todo.py` script contains automated test cases for a simple To-Do List application.

### Imports
```python
from unittest import TestCase
from examples.unit_test.todo_list.todo import ToDo
from examples.unit_test.todo_list import operations
from guara.transaction import Application
from guara import it
```

### Test Class: `TestToDo`
```python
class TestToDo:
    def setup_method(self, method):
        self._todo = Application(ToDo())
```
- Initializes a `To-Do List` application instance using Guara's transaction-based approach.

---

## Notes
- The **Guara framework** is used to structure tests using transactions, making it easy to reuse test logic.
- The **Async To-Do List tests** are fully **asynchronous**, requiring `pytest-asyncio`.
- The **Calculator tests** support multiple test frameworks, including `unittest` and `Testify`.
- The **To-Do List tests** cover additional transactions like `PrintDict` and `GetBy`.


