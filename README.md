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
- [Framework in action](#Framework-in-action)<br>
- [Installation](#Installation)<br>
- [Execution](#Execution)<br>
- [Tutorial](https://github.com/douglasdcm/guara/tree/main/docs/TUTORIAL.md)<br>
- [Examples](https://github.com/douglasdcm/guara/tree/main/examples)<br>
- [The pattern explained](https://github.com/douglasdcm/guara/tree/main/docs/THE_PATTERN_EXPLAINED.md)<br>
- [Using other Web Drivers](https://github.com/douglasdcm/guara/tree/main/docs/MISCELANEOS.md#Using-other-Web-Drivers)<br>
- [Asynchronous execution](https://github.com/douglasdcm/guara/tree/main/docs/MISCELANEOS.md#Asynchronous-execution)<br>
- [ChatGPT assistance](https://github.com/douglasdcm/guara/tree/main/docs/MISCELANEOS.md#ChatGPT-assistance)<br>
- [Page Transactions and Page Objects Model](https://github.com/douglasdcm/guara/tree/main/docs/PT_AND_POM.md)
- [Non-testers usage](https://github.com/douglasdcm/guara/tree/main/docs/MISCELANEOS.md#Non-testers-usage)<br>
- [Contributing](#Contributing)<br>

# Syntax

<code>Application.at(apage.DoSomething [,with_parameter=value, ...]).asserts(it.Matches, a_condition)</code>

# Introduction
> [!IMPORTANT]
> Guará is the Python implementation of the design pattern `Page Transactions`. It is more of a programming pattern than a tool. It can be bound to any web driver other than Selenium. Check the examples [here](https://github.com/douglasdcm/guara/tree/main/examples)

The intent of this pattern is to simplify UI test automation. It was inspired by Page Objects, App Actions, and Screenplay. `Page Transactions` focus on the operations (transactions) a user can perform on a web page, such as Login, Logout, or Submit Forms.

## Demonstration
[![Watch the video](./docs/images/guara-demo.png)](https://www.youtube.com/watch?v=r2pCN2jG7Nw)


## Framework in action

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

    # At Info page asserts the text is present
    app.at(info.NavigateTo).asserts(
        it.Contains, "This project was born"
    )

    # At setup closes the web application
    app.at(setup.CloseApp)
```
The *ugly* code which calls the webdriver is like this:

```python
class ChangeToPortuguese(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)

    def do(self, **kwargs):
        self._driver.find_element(
            By.CSS_SELECTOR, ".btn:nth-child(3) > button:nth-child(1) > img"
        ).click()
        self._driver.find_element(By.CSS_SELECTOR, ".col-md-10").click()
        return self._driver.find_element(By.CSS_SELECTOR, "label:nth-child(1)").text
```

It is a very repetitive activity:
- Create a class representing the transaction, in this case, the transaction changes the language to Portuguese
- Inherits from `AbstractTransaction`
- Implements the `do` method
    - Optional: Returns the result of the transaction

Read more in [Tutorial](#tutorial)

# Installation
## Dependencies
- Python 3.11
- Selenium

This framework can be installed by
```shell
pip install guara
```

# Execution
It is recommended to use `pytest`

```shell
# Executes reporting the complete log
python -m pytest -o log_cli=1 --log-cli-level=INFO --log-format="%(asctime)s %(levelname)s %(message)s" --log-date-format="%Y-%m-%d %H:%M:%S"
```
> [!TIP]
> These options can also be customized through your `pytest.ini` file. Refer to [Pytest documentaion](https://docs.pytest.org/en/stable/how-to/logging.html).

**Outputs**
```shell
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

It also works well with other test frameworks. Check more details [here](https://github.com/douglasdcm/guara/blob/main/docs/TEST_FRAMEWORKS.md)

# Tutorial
Read the [step-by-step](https://github.com/douglasdcm/guara/blob/main/docs/TUTORIAL.md) to build your first automation with this framework.

# How you can help?

Here's how you can help with this:
- Star this project on GitHub.
- Tell your friends and colleagues about it.
- Share it on social media.
- Write a blog post about Guara.
- Take a look at the `good first issue` [here](https://github.com/douglasdcm/guara/issues), assign any to you and push the code.

# Contributing
Read the [Code of Conduct](https://github.com/douglasdcm/guara/blob/main/docs/CODE_OF_CONDUCT.md) before push new Merge Requests.<br>
Now, follow the steps in [Contributing](https://github.com/douglasdcm/guara/blob/main/docs/CONTRIBUTING.md) session.
