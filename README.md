# Guará

[![PyPI Downloads](https://static.pepy.tech/badge/guara)](https://pepy.tech/projects/guara)

<img src=https://github.com/douglasdcm/guara/raw/main/docs/images/guara.jpg width="300" height="300" />

Photo by <a href="https://unsplash.com/@matcfelipe?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Mateus Campos Felipe</a> on <a href="https://unsplash.com/photos/red-flamingo-svdE4f0K4bs?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>
      
________


[Scarlet ibis (Guará)](https://en.wikipedia.org/wiki/Scarlet_ibis)

The scarlet ibis, sometimes called red ibis (Eudocimus ruber), is a species of ibis in the bird family Threskiornithidae. It inhabits tropical South America and part of the Caribbean. In form, it resembles most of the other twenty-seven extant species of ibis, but its remarkably brilliant scarlet coloration makes it unmistakable. It is one of the two national birds of Trinidad and Tobago, and its Tupi–Guarani name, guará, is part of the name of several municipalities along the coast of Brazil.

# Contents
- [Syntax](#Syntax)<br>
- [Introduction](#Introduction)<br>
- [The pattern](#The-pattern)<br>
- [Framework in action](#Framework-in-action)<br>
- [Installation](#Installation)<br>
- [Execution](#Execution)<br>
- [Tutorial](#Tutorial)<br>
- [Using other Web Drivers](#Using-other-Web-Drivers)<br>
- [Asynchronous execution](#Asynchronous-execution)<br>
- [Contributing](#Contributing)<br>

# Syntax

<code>Application.at(apage.DoSomething [,with_parameter=value, ...]).asserts(it.Matches, a_condition)</code>

# Introduction
> [!IMPORTANT]
> Guará is the Python implementation of the desing pattern `Page Transactions`. It is more of a programming pattern than a tool. It can be bound to any web driver other than Selenium. Check the examples [here](https://github.com/douglasdcm/guara/tree/main/examples)

The intent of this pattern is to simplify UI test automation. It was inspired by Page Objects, App Actions, and Screenplay. `Page Transactions` focus on the operations (transactions) a user can perform on a web page, such as Login, Logout, or Submit Forms.

# The pattern
<p align="center">
    <img src="https://github.com/douglasdcm/guara/blob/main/docs/images/uml_abstract_transaction.png?raw=true" width="800" height="300" />
</p>

- `AbstractTransaction`: This is the class from which all transactions inherit. The `do` method is implemented by each transaction. In this method, calls to WebDriver are placed. If the method returns something, like a string, the automation can use it for assertions.

<p align="center">
    <img src="https://github.com/douglasdcm/guara/blob/main/docs/images/uml_iassertion.png?raw=true" width="800" height="300" />
</p>

- `IAssertion`: This is the interface implemented by all assertion classes.
- The `asserts` method of each subclass contains the logic to perform validations. For example, the `IsEqualTo` subclass compares the `result` with the expected value provided by the tester.
- Testers can inherit from this interface to add new subclasses of validations that the framework does not natively support. More details [here](https://github.com/douglasdcm/guara/blob/main/docs/TUTORIAL.md#extending-assertions).

<p align="center">
    <img src="https://github.com/douglasdcm/guara/blob/main/docs/images/uml_application.png?raw=true" width="600" height="200" />
</p>

- `Application`: This is the runner of the automation. It executes the `do` method of each transaction and validates the result using the `asserts` method.
- The `asserts` method receives a reference to an `IAssertion` instance. It implements the `Strategy Pattern (GoF)` to allow its behavior to change at runtime.
- Another important component of the `Application` is the `result` property. It holds the result of the transaction, which can be used by `asserts` or inspected by the test using the native built-in `assert` method.


## Framework in action

The idea is to group blocks of interactions into classes. These classes inherit from `AbstractTransaction` and override the `do` method.

Each transaction is passed to the `Application` instance, which provides the methods `at` and `asserts`. These are the only two methods necessary to orchestrate the automation. While it is primarily bound to `Selenium WebDriver`, experience shows that it can also be used to test REST APIs, unit tests and can be executed in asynchronous mode (check the [`examples`](https://github.com/douglasdcm/guara/tree/main/examples) folder).

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
    # to English and uses many assertions to validate the `result`
    result = app.at(home.ChangeToEnglish).result
    it.IsEqualto().asserts(result, content_in_english)
    it.Contains().asserts(result, content_in_english)

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
## Dependencies
- Python 3.11
- Selenium

This framework can be installed by
```
pip install guara
```

# Execution
It is recommended to use `pytest`

```
# Executes reporting the complete log
python -m pytest -o log_cli=1 --log-cli-level=INFO --log-format="%(asctime)s %(levelname)s %(message)s" --log-date-format="%Y-%m-%d %H:%M:%S"
```
> [!TIP]
> These options can also be customized through your `pytest.ini` file. Refer to [Pytest documentaion](https://docs.pytest.org/en/stable/how-to/logging.html).

**Outputs**
```
examples/web_ui/selenium/simple/test_local_page.py::TestLocalTransaction::test_local_page
--------------------------------------------------------------- live log setup ---------------------------------------------------------------
2025-01-09 06:39:41 INFO Transaction 'OpenApp'
2025-01-09 06:39:41 INFO  url: file:////...sample.html
2025-01-09 06:39:41 INFO  window_width: 1094
2025-01-09 06:39:41 INFO  window_height: 765
2025-01-09 06:39:41 INFO  implicitly_wait: 0.5
2025-01-09 06:39:41 INFO Assertion 'IsEqualTo'
2025-01-09 06:39:41 INFO  actual:   'Sample page'
2025-01-09 06:39:41 INFO  expected: 'Sample page'
--------------------------------------------------------------- live log call ----------------------------------------------------------------
2025-01-09 06:39:41 INFO Transaction 'SubmitText'
2025-01-09 06:39:41 INFO  text: cheese
2025-01-09 06:39:41 INFO Assertion 'IsEqualTo'
2025-01-09 06:39:41 INFO  actual:   'It works! cheese!'
2025-01-09 06:39:41 INFO  expected: 'It works! cheese!'
2025-01-09 06:39:41 INFO Transaction 'SubmitText'
2025-01-09 06:39:41 INFO  text: cheese
2025-01-09 06:39:41 INFO Assertion 'IsNotEqualTo'
2025-01-09 06:39:41 INFO  actual:   'It works! cheesecheese!'
2025-01-09 06:39:41 INFO  expected: 'Any'
PASSED                                                                                                                                 [100%]
------------------------------------------------------------- live log teardown --------------------------------------------------------------
2025-01-09 06:39:41 INFO Transaction 'CloseApp'

```

# Tutorial
Read the [step-by-step](https://github.com/douglasdcm/guara/blob/main/docs/TUTORIAL.md) to build your first automation with this framework.

# Using other Web Drivers

It is possible to run Guara using other Web Drivers like [Caqui](https://github.com/douglasdcm/caqui) and [Playwright](https://playwright.dev/python/docs/intro). Check the requirements of each Web Driver before execute it. For example, Playwright requires the installation of browsers separetly.

# Asynchronous execution
The core code was extended to allow asynchronous executions. Get more details [here](https://github.com/douglasdcm/guara/tree/main/docs/ASYNC.md)


# How you can help?

Here's how you can help with this:
- Star this project on GitHub.
- Tell your friends and colleagues about it.
- Share it on social media
- Write a blog post about Guara.

# Contributing
Read the [Code of Conduct](https://github.com/douglasdcm/guara/blob/main/docs/CODE_OF_CONDUCT.md) before push new Merge Requests.<br>
Now, follow the steps in [Contributing](https://github.com/douglasdcm/guara/blob/main/docs/CONTRIBUTING.md) session.