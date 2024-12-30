# Canonical implementation
This is the simplest implementation to warm up the framework. It uses the built-in `setup` transaction to open the web page of Google, to assert the title of the page is `Google` and to close the web application. More details about each component of the framework are explained in further sessions.

```python
from selenium import webdriver
from guara import it
from guara import setup
from guara.transaction import Application


def test_canonical():
    app = Application(webdriver.Chrome())
    app.at(
        setup.OpenApp,
        url="http://www.google.com",
    ).asserts(it.IsEqualTo, "Google")
    app.at(setup.CloseApp)
```

# Basic pratical example

This is a basic search of the term "guara" on Google. To follow the steps create the files `home.py` and `test_tutorial.py` at the same folder.

```python
# home.py

from selenium.webdriver.common.by import By
from guara.transaction import AbstractTransaction


class Search(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)

    def do(self, text):
        # Sends the received text to the textbox in the UI
        self._driver.find_element(By.NAME, "q").send_keys(text)
        
        # Click the button to search
        self._driver.find_element(By.NAME, "btnK").click()
        
        # Waits the next page appears and returns the label of the first tab "All".
        # It will be used by assertions in the next sessions.  
        return self._driver.find_element(
            By.CSS_SELECTOR, ".Ap1Qsc > a:nth-child(1) > div:nth-child(1)"
        ).text
```
- `class Search`: is a concret transation. Notice that the name of the class is an action and not a noun as usually saw in OOP. It is intentional to make the statments in the test more natural.
- `def __init__`: is the same for all transactions. It passes the `driver` to the `AbstractTransaction`.
- `def do`: is the *ugly* implementation of the memthod. It uses the private attribute `self._driver` inherited from `AbstractTransaction` to call `find_element`, `send_keys`, `click` and `text` from Selenium Webdriver. Notice the parameter `text`. It is received from the automation via `kwargs`. More details in further sessions.

```python
# test_tutorial.py

import pytest

# Imports the module with the transactions of the Home page
import home

from selenium import webdriver

# Imports the Application to buld and run the automation
from guara.transaction import Application

# Imports the module with the strategies to asset the result
from guara import it

# Imports the module which contains the built-in transactions to open
# and close the web application using Selenium
from guara import setup

@pytest.fixture
def setup_app():
    # Instantiates the Application to run the automation
    app = Application(webdriver.Chrome())

    # Some intersting things happen here.
    # The framework is used to setup the web application.
    # The method `at` from `app` is the key point here as it
    # receives a transaction (AbstractTransaction) and its `kwargs`.
    # Internaly `at` executes the `do` method of the transaction and
    # holds the result in the property `result` which is going to be
    # presented soon.
    # `setup.OpenApp` is a built-in transaction.
    # The `url` is passed to the `at` method by `kwargs`.
    # The result returned by `at` is asseted by `asserts`
    # using the strategy `it.IsEqualTo`.
    app.at(
        setup.OpenApp,
        url="http://www.google.com",
    ).asserts(it.IsEqualTo, "Google")
    yield app

    # Uses the built-in `setup.CloseApp` to close the web application
    app.at(setup.CloseApp)


def test_google_search(setup_app):
    app = setup_app

    # With the `app` received from the fixture the similar things
    # explaned previouslly in the fixture happens.
    # The transaction `home.Search` with the parameter `text`
    # is passed to `at` and the result is asserted by `asserts` with
    # the strategy `it.IsEqualTo`
    app.at(home.Search, text="guara").asserts(it.IsEqualTo, "All")

```
- `class Application`: is the runner of the automation. It receives the `driver` and passes it hand by hand to transactions.
- `def at`: receives the transaction created on `home.py` and its parameters. Notice the usage of the module name `home` to make the readability of the statement as plain English. The parameters are passed explictly for the same purpose. So the `at(home.Search, text="guara")` is read `At home [page] search [for] text "guara"`. The terms `page` and `for` could be added to the implementation to make it more explict, like `at(homePage.Search, for_text="guara")`. This is a decision the tester may make while developing the transactions. 
- `def asserts`: receives a strategy to compare the result against an expected value. Again, the focous on readability is kept. So, `asserts(it.IsEqualTo, "All")` can be read `asserts it is equal to 'All'`
- `it.IsEqualTo`: is one of the strategies to compare the actual and the expected result. Other example is the `it.Contains` which checks if the value is present in the page. Notice that the assertion is very simple: it validates just one value. The intention here is keep the framework simple, but robust. The tester is able to extend the strategies inheriting from `IAssertion`.

# Extending assertions
The strategies to assert the result can e extended by inheriting from `IAssertion` as following:

```python
# The code is the same of the previous session.
# The unnecessary details were not duplicated
# import IAssertion 
from guara.transaction import Application, IAssertion

# Implements a new assertion to check variations of the expected value
class IsEqualToVariationsOf(IAssertion):
    def __init__(self):
        super().__init__()

    def asserts(self, actual, expected):
        assert actual.lower() == expected.lower()

def test_google_search(setup_app):
    app = setup_app
    
    # The new assertion is used to check variations of 'All', like 'aLL' or 'ALL'
    app.at(home.Search, text="guara").asserts(IsEqualToVariationsOf, "All")

```

# Debbuging

Errors in assertions are printed like this. Got the same example above. Notice the `actual` and `expected` values do not match.
```python

_____________________________________________________________ test_google_search _____________________________________________________________

setup_app = <guara.transaction.Application object at 0x7f3c42bf6f90>

    def test_google_search(setup_app):
        app = setup_app
>       app.at(home.Search, text="guara").asserts(IsEqualToVariationsOf, "ALL")

test_tmp.py:30: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
venv/lib/python3.11/site-packages/guara/transaction.py:27: in asserts
    it().asserts(self._result, expected)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <test_tmp.IsEqualToVariationsOf object at 0x7f3c4349fc10>, actual = 'alls', expected = 'all'

    def asserts(self, actual, expected):
>       assert actual.lower() == expected.lower()
E       AssertionError: assert 'alls' == 'all'
E         
E         - alls
E         ?    -
E         + all

```

# Advanced
For more examples of implentations check the [`tests`](https://github.com/douglasdcm/guara/blob/main/tests) folder.