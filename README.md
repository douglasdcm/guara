# Guará

<img src=https://github.com/douglasdcm/guara/raw/main/image.jpg width="300" height="300" />

Photo by <a href="https://unsplash.com/@matcfelipe?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Mateus Campos Felipe</a> on <a href="https://unsplash.com/photos/red-flamingo-svdE4f0K4bs?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>
      
________


[Scarlet ibis (Guará)](https://en.wikipedia.org/wiki/Scarlet_ibis)

The scarlet ibis, sometimes called red ibis (Eudocimus ruber), is a species of ibis in the bird family Threskiornithidae. It inhabits tropical South America and part of the Caribbean. In form, it resembles most of the other twenty-seven extant species of ibis, but its remarkably brilliant scarlet coloration makes it unmistakable. It is one of the two national birds of Trinidad and Tobago, and its Tupi–Guarani name, guará, is part of the name of several municipalities along the coast of Brazil.

# Syntax

<code>Application.at(apage.DoSomething [,with_parameter=value, ...]).asserts(it.Matches, a_condition)</code>

# Introduction
> [!IMPORTANT]
> Guará is the Python implementation of the desing pattern `Page Transactions`. It is more of a programming pattern than a tool. It can be bound to any web driver other than Selenium.. Check the examples [here](https://github.com/douglasdcm/guara/tree/main/tests)

The intent of this pattern is to simplify UI test automation. It was inspired by Page Objects, App Actions, and Screenplay. `Page Transactions` focus on the operations (transactions) a user can perform on a web page, such as Login, Logout, or Submit Forms.

# The pattern
<p align="center">
    <img src="https://github.com/douglasdcm/guara/blob/main/uml_abstract_transaction.png?raw=true" width="800" height="300" />
</p>

- `AbstractTransaction`: This is the class from which all transactions inherit. The `do` method is implemented by each transaction. In this method, calls to WebDriver are placed. If the method returns something, like a string, the automation can use it for assertions.

<p align="center">
    <img src="https://github.com/douglasdcm/guara/blob/main/uml_iassertion.png?raw=true" width="800" height="300" />
</p>

- `IAssertion`: This is the interface implemented by all assertion classes.
- The `asserts` method of each subclass contains the logic to perform validations. For example, the `IsEqualTo` subclass compares the `result` with the expected value provided by the tester.
- Testers can inherit from this interface to add new subclasses of validations that the framework does not natively support. More details [here](https://github.com/douglasdcm/guara/blob/main/TUTORIAL.md#extending-assertions).

<p align="center">
    <img src="https://github.com/douglasdcm/guara/blob/main/uml_application.png?raw=true" width="600" height="200" />
</p>

- `Application`: This is the runner of the automation. It executes the `do` method of each transaction and validates the result using the `asserts` method.
- The `asserts` method receives a reference to an `IAssertion` instance. It implements the `Strategy Pattern (GoF)` to allow its behavior to change at runtime.
- Another important component of the `Application` is the `result` property. It holds the result of the transaction, which can be used by `asserts` or inspected by the test using the native built-in `assert` method.


## Framework in action

The idea is to group blocks of interactions into classes. These classes inherit from `AbstractTransaction` and override the `do` method.

Each transaction is passed to the `Application` instance, which provides the methods `at` and `asserts`. These are the only two methods necessary to orchestrate the automation. While it is primarily bound to `Selenium WebDriver`, experience shows that it can also be used to test REST APIs, unit tests and can be executed in asynchronous mode (check the [`tests`](https://github.com/douglasdcm/guara/tree/main/tests) folder).

When the framework is in action, it follows a highly repetitive pattern. Notice the use of the `at` method to invoke transactions and the `asserts` method to apply assertion strategies. Also, the automation is described in plain English improving the comprehention of the code.

```python
from selenium import webdriver
from pages import home, contact, info
from guara.transaction import Application
from guara import it, setup

def test_sample_web_page():
    # Instantiates the Application with a driver
    app = Application(webdriver.Chrome())
    
    # At setup opens the web application
    app.at(setup.OpenApp, url="https://anyhost.com/",)
    
    # At Home page changes the language to Portuguese and asserts its content
    app.at(home.ChangeToPortuguese).asserts(it.IsEqualTo, content_in_portuguese)
    
    # Still at Home page changes the language
    # to English and uses native assertion to validate the `result`
    assert app.at(home.ChangeToEnglish).result == content_in_english
    
    # At Info page asserts the text is present
    app.at(info.NavigateTo).asserts(
        it.Contains, "This project was born"
    )

    # At setup closes the web application
    app.at(setup.CloseApp)
```
- `setup.OpenApp` and `setup.CloseApp` are part of the framework and provide basic implementation to open and close the web application using Selenium Webdriver.
- `it` is the module which contains the concret assertions.

The *ugly* code which calls the webdriver is like this:

```python
class ChangeToPortuguese(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)

    # Implements the `do` method and returns the `result`
    def do(self, **kwargs):
        self._driver.find_element(
            By.CSS_SELECTOR, ".btn:nth-child(3) > button:nth-child(1) > img"
        ).click()
        self._driver.find_element(By.CSS_SELECTOR, ".col-md-10").click()
        return self._driver.find_element(By.CSS_SELECTOR, "label:nth-child(1)").text
```

Again, it is a very repetivite activity:
- Create a class representing the transaction, in this case, the transaction changes the language to Portuguese
- Inherits from `AbstractTransaction`
- Implementes the `do` method
    - Optinonal: Returns the result of the transaction

Read more in [Tutorial](#tutorial)

# Installation
This framework can be installed by

```
pip install guara
```

# Execution with Selenium
It is recommended to use `pytest`

```
# Executes reporting the complete log
python -m pytest -o log_cli=1 --log-cli-level=INFO
```
**Outputs**
```
tests/web_ui_local/test_local_page.py::TestLocalTransaction::test_local_page 
--------------------------------------------------------------- live log setup ---------------------------------------------------------------
INFO     guara.transaction:transaction.py:26 Transaction 'OpenApp'
INFO     guara.transaction:transaction.py:28  url: file:////sample.html
INFO     guara.transaction:transaction.py:28  window_width: 1094
INFO     guara.transaction:transaction.py:28  window_hight: 765
INFO     guara.transaction:transaction.py:28  implicitly_wait: 0.5
--------------------------------------------------------------- live log call ----------------------------------------------------------------
INFO     guara.transaction:transaction.py:26 Transaction 'SubmitText'
INFO     guara.transaction:transaction.py:28  text: bla
INFO     guara.transaction:transaction.py:34 Assertion 'IsEqualTo'
INFO     guara.transaction:transaction.py:35  actual:   'It works! bla!'
INFO     guara.transaction:transaction.py:36  expected: 'It works! bla!'
INFO     guara.transaction:transaction.py:37 ---
INFO     guara.transaction:transaction.py:26 Transaction 'SubmitText'
INFO     guara.transaction:transaction.py:28  text: bla
INFO     guara.transaction:transaction.py:34 Assertion 'IsNotEqualTo'
INFO     guara.transaction:transaction.py:35  actual:   'It works! blabla!'
INFO     guara.transaction:transaction.py:36  expected: 'Any'
INFO     guara.transaction:transaction.py:37 ---
PASSED
```

# Execution with [Caqui](https://github.com/douglasdcm/caqui) (async)
```
# runs the example TestAsyncTransaction.
# Go to test_async.py to check requisites to start Caqui
python -m pytest -n auto -k TestAsyncTransaction -s
```
Outputs
```
4 workers [2 items]
..
============================================================= 2 passed in 3.56s ==============================================================

```

# Tutorial
Read the [step-by-step](https://github.com/douglasdcm/guara/blob/main/TUTORIAL.md) to build your first automation with this framework.

# Contributing
Read the [Code of Conduct](https://github.com/douglasdcm/guara/blob/main/CODE_OF_CONDUCT.md) before push new Merge Requests.
Now, follow the steps in [Contributing](https://github.com/douglasdcm/guara/blob/main/CONTRIBUTING.md) session.
