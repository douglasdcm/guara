# Guará

<img src=https://github.com/douglasdcm/guara/blob/main/image.jpg width="300" height="300" />

Photo by <a href="https://unsplash.com/@matcfelipe?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Mateus Campos Felipe</a> on <a href="https://unsplash.com/photos/red-flamingo-svdE4f0K4bs?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>
      
________


[Scarlet ibis (Guará)](https://en.wikipedia.org/wiki/Scarlet_ibis)

The scarlet ibis, sometimes called red ibis (Eudocimus ruber), is a species of ibis in the bird family Threskiornithidae. It inhabits tropical South America and part of the Caribbean. In form, it resembles most of the other twenty-seven extant species of ibis, but its remarkably brilliant scarlet coloration makes it unmistakable. It is one of the two national birds of Trinidad and Tobago, and its Tupi–Guarani name, guará, is part of the name of several municipalities along the coast of Brazil.

________

Guará is an implementation of the `Page Transactions` pattern. The intent of this pattern is to simplify UI test automation. It was inspired by Page Objects, App Actions, and Screenplay. `Page Transactions` focus on the operations (transactions) a user can perform on a web page, such as Login, Logout, or Submit Forms. The idea is to group blocks of interactions into classes. These classes inherit from `AbstractTransaction` and override the `do` method.

Each transaction is passed to the `Application` instance, which provides the methods `at` and `asserts`. These are the only two methods necessary to orchestrate the automation. While it is primarily bound to `Selenium WebDriver`, experience shows that it can also be used to test REST APIs and unit tests, for example (check the `tests` folder).

Here is the base implementation of the framework:

```python

from typing import Any, NoReturn
from selenium.webdriver.remote.webdriver import WebDriver
from guara.it import IAssertion


class AbstractTransaction:
    def __init__(self, driver: WebDriver):
        self._driver = driver

    def do(self, **kwargs) -> Any | NoReturn:
        raise NotImplementedError


class Application:
    def __init__(self, driver):
        self._driver = driver

    @property
    def result(self):
        return self._result

    def at(self, transaction: AbstractTransaction, **kwargs):
        self._result = transaction(self._driver).do(**kwargs)
        return self

    def asserts(self, it: IAssertion, expected):
        it().asserts(self._result, expected)
        return self
```

- `AbstractTransaction`: This is the class from which all transactions inherit. The `do` method is implemented by each transaction. In this method, calls to WebDriver are placed. If the method returns something, like a string, the automation can use it for assertions.  

- `Application`: This is the runner of the automation. It executes the `do` method of each transaction and validates the result using the `asserts` method.  
  - The `asserts` method receives a reference to an `IAssertion` instance. It implements the `Strategy Pattern` to allow its behavior to change at runtime.  
  - Another important component of the `Application` is the `result` property. It holds the result of the transaction, which can be used by `asserts` or inspected by the test using the native built-in `assert` method.  

- `IAssertion`: This is the interface implemented by all assertion classes.  
  - The `asserts` method of each subclass contains the logic to perform validations. For example, the `IsEqualTo` subclass compares the `result` with the expected value provided by the tester.  
  - Testers can extend this interface to add new validations that the framework does not natively support.  

When the framework is in action, it follows a highly repetitive pattern. Notice the use of the `at` method to invoke transactions and the `asserts` method to apply assertion strategies. Also, the automation is describe in plain English improving the comprehention of the code.

```python
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
    app.at(info.Navgigate).asserts(
        it.Contains, "This project was born"
    )

    # At setup closes the web application
    app.at(setup.CloseApp)
```
- `setup.OpenApp` and `setup.CloseApp` are part of the framework and provide basic implementation to open and close the web application using Selenium Webdriver.

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
________

# Tutorial
Read the [step-by-step](https://github.com/douglasdcm/guara/blob/main/TUTORIAL.md) to build your first automation with this framework.

# Contributing
Read the [Code of Conduct](https://github.com/douglasdcm/guara/blob/main/CODE_OF_CONDUCT.md) before push new Merge Requests.
Now, follow the steps in [Contributing](https://github.com/douglasdcm/guara/blob/main/CONTRIBUTING.md) session.