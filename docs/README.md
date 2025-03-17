# Guará

[![PyPI Downloads](https://static.pepy.tech/badge/guara)](https://pepy.tech/projects/guara) ![GitHub Repo stars](https://img.shields.io/github/stars/douglasdcm/guara?style=social) ![GitHub forks](https://img.shields.io/github/forks/douglasdcm/guara) [![Build Status](https://cdn.prod.website-files.com/5e0f1144930a8bc8aace526c/65dd9eb5aaca434fac4f1c7c_Build-Passing-brightgreen.svg)](https://github.com/douglasdcm/guara/actions) [![License: MIT](https://cdn.prod.website-files.com/5e0f1144930a8bc8aace526c/65dd9eb5aaca434fac4f1c34_License-MIT-blue.svg)]([/LICENSE](https://github.com/douglasdcm/guara/blob/main/LICENSE))

# Syntax

<code>Application.at(apage.DoSomething [,with_parameter=value, ...]).asserts(it.Matches, a_condition)</code>

Guará is the Python implementation of the design pattern `Page Transactions`. The intent of this pattern is to simplify UI test automation. It was inspired by Page Objects, App Actions, and Screenplay. `Page Transactions` focus on the operations (transactions) a user can perform on a web page, such as Login, Logout, or Submit Forms.

## Demonstration
[![Watch the video](./images/guara-demo.png)](https://www.youtube.com/watch?v=r2pCN2jG7Nw)


## Sample code

```python
from selenium import webdriver
from pages import home, contact, info, setup
from guara.transaction import Application
from guara import it

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

The idea is to group blocks of interactions into classes. Each transaction is passed to the `Application` instance, which provides the methods `at` and `asserts`. These are the only two methods necessary to orchestrate the automation.

While it is primarily bound to `Selenium WebDriver`, experience shows that it can also be used to test REST APIs, unit tests and can be executed in asynchronous mode. The automation is described in plain English improving the comprehension of the code.

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

These classes inherit from `AbstractTransaction` and override the `do` method.


Again, it is a very repetitive activity:
- Create a class representing the transaction, in this case, the transaction changes the language to Portuguese
- Inherits from `AbstractTransaction`
- Implements the `do` method
    - Optional: Returns the result of the transaction

# Installation
## Dependencies
- Python 3.8+

This framework can be installed by
```shell
pip install guara
```

# Execution
Using `pytest`

```shell
python -m pytest
```

**Outputs**
```shell
examples/web_ui/selenium/simple/test_local_page.py::TestLocalTransaction::test_local_page
--------------------------------------------------------------- live log setup
2025-01-09 06:39:41 INFO Transaction 'OpenApp'
2025-01-09 06:39:41 INFO  url: file:////...sample.html
2025-01-09 06:39:41 INFO  window_width: 1094
2025-01-09 06:39:41 INFO  window_height: 765
2025-01-09 06:39:41 INFO  implicitly_wait: 0.5
2025-01-09 06:39:41 INFO Assertion 'IsEqualTo'
2025-01-09 06:39:41 INFO  actual:   'Sample page'
2025-01-09 06:39:41 INFO  expected: 'Sample page'
--------------------------------------------------------------- live log call
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
PASSED
------------------------------------------------------------- live log teardown
2025-01-09 06:39:41 INFO Transaction 'CloseApp'

```

# Tutorial
Read the [step-by-step](https://github.com/douglasdcm/guara/blob/main/docs/TUTORIAL.md) to build your first automation with this framework.

# Using other Web Drivers

It is possible to run Guara using other Web Drivers like [Caqui](https://github.com/douglasdcm/caqui) and [Playwright](https://playwright.dev/python/docs/intro). Check the requirements of each Web Driver before execute it. For example, Playwright requires the installation of browsers separately.

# The pattern explained

Check more details [here](https://github.com/douglasdcm/guara)

# Contributing
Read the [Code of Conduct](https://github.com/douglasdcm/guara/blob/main/docs/CODE_OF_CONDUCT.md) before push new Merge Requests.<br>

Now, follow the steps in [Contributing](https://github.com/douglasdcm/guara/blob/main/docs/CONTRIBUTING.md) session.
