# The pattern Explained
<p align="center">
    <img src="https://github.com/douglasdcm/guara/blob/main/docs/images/uml_abstract_transaction.png?raw=true" width="800" height="300" />
</p>

- `AbstractTransaction`: This is the class from which all transactions inherit. The `do` method is implemented by each transaction. In this method, calls to WebDriver are placed. If the method returns something, like a string, the automation can use it for assertions.
- `OpenApp` and `CloseApp` are examples of concrete transactions.

<p align="center">
    <img src="https://github.com/douglasdcm/guara/blob/main/docs/images/uml_iassertion.png?raw=true" width="800" height="300" />
</p>

- `IAssertion`: This is the interface implemented by all concrete assertions.
- The `asserts` method of each concrete assertion contains the logic to perform validations. For example, the `IsEqualTo` concrete assertion compares the `result` with the expected value provided by the tester.
- Testers can inherit from this interface to add new sub-classes of validations that the framework does not natively support. More details [here](https://github.com/douglasdcm/guara/blob/main/docs/TUTORIAL.md#extending-assertions).

<p align="center">
    <img src="https://github.com/douglasdcm/guara/blob/main/docs/images/uml_application.png?raw=true" width="600" height="200" />
</p>

- `Application`: This is the runner of the automation. It executes the `do` method of each transaction and validates the result using the `asserts` method.
- The `asserts` method receives a reference to an `IAssertion` instance. It implements the `Strategy Pattern (GoF)` to allow its behavior to change at runtime.
- Another important component of the `Application` is the `result` property. It holds the result of the transaction, which can be used by `asserts` or inspected by the test using the native built-in `assert` method.

# Using it
The idea is to group blocks of interactions into classes. These classes inherit from `AbstractTransaction` and override the `do` method.

Each transaction is passed to the `Application` instance, which provides the methods `at` and `asserts`. These are the only two methods necessary to orchestrate the automation. While it is primarily bound to `Selenium WebDriver`, experience shows that it can also be used to test REST APIs, unit tests and can be executed in asynchronous mode (check the [`examples`](https://github.com/douglasdcm/guara/tree/main/examples) folder).

When the framework is in action, it follows a highly repetitive pattern. Notice the use of the `at` method to invoke transactions and the `asserts` method to apply assertion strategies. Also, the automation is described in plain English improving the comprehension of the code.


```python
from selenium import webdriver
from pages import home, contact, info, setup
from guara.transaction import Application
from guara import it

def test_sample_web_page():
    app = Application(webdriver.Chrome())
    app.at(setup.OpenApp, url="https://anyhost.com/",)
    app.at(home.ChangeToPortuguese).asserts(it.IsEqualTo, content_in_portuguese)
    app.at(home.ChangeToEnglish).asserts(IsEqualto, content_in_english)
    app.at(info.NavigateTo).asserts(
        it.Contains, "This project was born"
    )
    app.at(setup.CloseApp)
```
- `it` is the module which contains the concrete assertions.

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

Again, it is a very repetitive activity:
- Create a class representing the transaction, in this case, the transaction changes the language to Portuguese
- Inherits from `AbstractTransaction`
- Implements the `do` method
    - Optional: Returns the result of the transaction
