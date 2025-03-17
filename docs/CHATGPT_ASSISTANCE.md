# Using ChatGPT with Page Transactions

As `Page Transactions` pattern is a new term. ChatGPT will not find a reference to it. But, it is not an excuse to not use the pattern. Teaching ChatGPT about the pattern is very easy and fast and the result is pretty much accurate.

1. Go to [ChatGPT](https://chatgpt.com/) page and login with your account. Create a new one if necessary.
2. Go to [Guara README.md](https://github.com/douglasdcm/guara/tree/main/docs/THE_PATTERN_EXPLAINED.md) and copy the raw content ![alt text](images/copy_raw_content.png)
3. Paste the following statements in the ChatGPT prompt
```
Given the explanation of the pattern Page Transactions after the dots let me know what you understood
...
<the raw content you copied>
```
4. Check it understanding and continue
5. Now that ChatGPT knows about the new pattern. Ask it to organize your code using it
```
Based on your understanding about the pattern Page Transactions organize the code after the dots
...
<your raw code>
```
6. Check if

- `guara` is part of the imports
- `Application` is used to orchestrate the code execution with `at` and `asserts`
7. Make necessary adjustments if necessary
8. Done! Your code is in the new pattern.

# Here is a practical example

## Raw code in Selenium

```python
import random
import pathlib
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_sample_page():
    file_path = pathlib.Path(__file__).parent.resolve()
    driver = webdriver.Chrome()

    driver.get(f"file:///{file_path}/sample.html")

    title = driver.title
    # assert title == "Web form"
    assert title == "Sample page"

    driver.implicitly_wait(0.5)

    # text_box = driver.find_element(by=By.NAME, value="input")
    text_box = driver.find_element(by=By.ID, value="input")
    submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

    text = ["cheese", "selenium", "test", "bla", "foo"]
    text_box.send_keys(text[random.randrange(len(text))])
    from_input = text_box.get_attribute("value")
    submit_button.click()

    message = driver.find_element(by=By.ID, value="result")
    value = message.text
    # assert value == "It workls! Selenium!"
    assert value == f"It works! {from_input}!"

    driver.quit()
```

## It is the output of ChatGPT

To organize this code following the Page Transactions pattern, we need to abstract transactions (e.g., opening the page, interacting with input fields, and validating results) into reusable classes that inherit from AbstractTransaction. The test logic should then use the Application class to orchestrate these transactions.

Here's the organized code:

```python
import random
import pathlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from guara.transaction import AbstractTransaction, Application
from guara import it


# Transaction: Open the sample page
class OpenSamplePage(AbstractTransaction):
    def __init__(self, driver, file_path):
        super().__init__(driver)
        self.file_path = file_path

    def do(self, **kwargs):
        self._driver.get(f"file:///{self.file_path}/sample.html")
        self._driver.implicitly_wait(0.5)
        return self._driver.title


# Transaction: Submit text to the form
class SubmitText(AbstractTransaction):
    def do(self, **kwargs):
        text = kwargs.get("text", "")
        text_box = self._driver.find_element(by=By.ID, value="input")
        submit_button = self._driver.find_element(by=By.CSS_SELECTOR, value="button")

        text_box.send_keys(text)
        from_input = text_box.get_attribute("value")
        submit_button.click()
        return from_input


# Transaction: Validate the result message
class ValidateResult(AbstractTransaction):
    def do(self, **kwargs):
        expected_text = kwargs.get("expected_text", "")
        message = self._driver.find_element(by=By.ID, value="result")
        return message.text == f"It works! {expected_text}!"

# Transaction to close the application
class CloseApplication(AbstractTransaction):
    def do(self, screenshot_filename: str = "./captures/guara-capture") -> None:
        self._driver.get_screenshot_as_file(f"{screenshot_filename}-{datetime.now()}.png")
        self._driver.quit()

# Test Case
def test_sample_page():
    file_path = pathlib.Path(__file__).parent.resolve()
    driver = webdriver.Chrome()

    # Instantiate the Application
    app = Application(driver)

    # Open the sample page and assert the title
    title = app.at(OpenSamplePage, file_path=file_path).result
    app.asserts(it.IsEqualTo, "Sample page")

    # Submit text and validate the result
    text_choices = ["cheese", "selenium", "test", "bla", "foo"]
    selected_text = random.choice(text_choices)

    app.at(SubmitText, text=selected_text)
    app.at(ValidateResult, expected_text=selected_text).asserts(it.IsTrue)

    # Close the application
    app.at(CloseApplication)

```

Explanation:

Transactions:
    OpenSamplePage: Handles the logic to open the web page and optionally returns the page title.
    SubmitText: Interacts with the input field and submits the form, returning the entered text.
    ValidateResult: Validates that the result message matches the expected format.
    CloseApplication: Closes the application

Application:
    Orchestrates the transactions using the at method and applies assertions using the asserts method.

Test Flow:
    The test script uses Application to execute transactions in a logical sequence.
    Assertions are modular, readable, and reusable.

Reusability:
    The transaction classes are reusable for other tests involving similar interactions. This modular approach reduces duplication and enhances maintainability.

Let me know if you'd like further adjustments!

## Make necessary adjustments

Notice the class `OpenSamplePage` has the parameter `file_path` with is not following the functional usage of the pattern and the assertion `it.IsTrue` does not exist in Guara core (yet). The new assertion introduced by the AI was a good induction. 

It is still possible to use ChatGPT to fix the issues. For example:

```
The code has some inconsistencies listed after the dots. Based on the list, give corrections in the code and outputs it to me 
....
- The transaction constructors does not allow other parameters than the `driver`. Any necessary parameters should be placed in the 'do' method
- The module 'gura.it' has no function 'IsTrue'. Check the explanation after the slashes to know how to build a new custom assertion 'IsTrue' and replace 'it.IsTrue' by 'IsTrue'

 \\\\\
# Got from https://github.com/douglasdcm/guara/blob/main/docs/TUTORIAL.md#extending-assertions

The strategies to assert the result can e extended by inheriting from IAssertion as following:

# The code is the same of the previous session.
# The unnecessary details were not duplicated
# import IAssertion 
from guara.transaction import Application, IAssertion

# Implements a new assertion to check variations of the expected value
class IsEqualToVariationsOf(IAssertion):
    def __init__(self):
        super().__init__()

    def asserts(self, actual, expected):
        if actual.lower() == expected.lower():
            return True
        raises AssertionError

def test_google_search(setup_app):
    app = setup_app
    
    # The new assertion is used to check variations of 'All', like 'aLL' or 'ALL'
    app.at(home.Search, text="guara").asserts(IsEqualToVariationsOf, "All") 
```

### The output

Here is the corrected and updated code based on the feedback:
Updates:

Transaction Constructors: Now accept only the driver parameter. Any additional parameters are passed to the do method.
Custom Assertion (IsTrue): A new custom assertion class is implemented, inheriting from IAssertion. This replaces the invalid it.IsTrue.

Corrected Code:

```python
import random
import pathlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from guara.transaction import AbstractTransaction, Application, IAssertion
from guara import it


# Custom Assertion: Checks if the actual value is True
class IsTrue(IAssertion):
    def __init__(self):
        super().__init__()

    def asserts(self, actual, expected=None):
        if actual is not True:
            raise AssertionError(f"Expected True but got {actual}")


# Transaction: Open the sample page
class OpenSamplePage(AbstractTransaction):
    def do(self, **kwargs):
        file_path = kwargs.get("file_path")
        self._driver.get(f"file:///{file_path}/sample.html")
        self._driver.implicitly_wait(0.5)
        return self._driver.title


# Transaction: Submit text to the form
class SubmitText(AbstractTransaction):
    def do(self, **kwargs):
        text = kwargs.get("text", "")
        text_box = self._driver.find_element(by=By.ID, value="input")
        submit_button = self._driver.find_element(by=By.CSS_SELECTOR, value="button")

        text_box.send_keys(text)
        from_input = text_box.get_attribute("value")
        submit_button.click()
        return from_input


# Transaction: Validate the result message
class ValidateResult(AbstractTransaction):
    def do(self, **kwargs):
        expected_text = kwargs.get("expected_text", "")
        message = self._driver.find_element(by=By.ID, value="result")
        actual_text = message.text
        return actual_text == f"It works! {expected_text}!"


# Transaction to close the application
class CloseApplication(AbstractTransaction):
    def do(self, screenshot_filename: str = "./captures/guara-capture") -> None:
        self._driver.get_screenshot_as_file(f"{screenshot_filename}-{datetime.now()}.png")
        self._driver.quit()

# Test Case
def test_sample_page():
    file_path = pathlib.Path(__file__).parent.resolve()
    driver = webdriver.Chrome()

    # Instantiate the Application
    app = Application(driver)

    # Open the sample page and assert the title
    title = app.at(OpenSamplePage, file_path=str(file_path)).result
    app.asserts(it.IsEqualTo, "Sample page")

    # Submit text and validate the result
    text_choices = ["cheese", "selenium", "test", "bla", "foo"]
    selected_text = random.choice(text_choices)

    app.at(SubmitText, text=selected_text)
    result = app.at(ValidateResult, expected_text=selected_text).result

    # Use the custom assertion to validate that the result is True
    app.asserts(IsTrue, result)

    # Close the application
    app.at(CloseApplication)
```

# Conclusion
The code needs some polishiment, like the `title` variable is never used, the occurrences of `app.asserts` can be suppressed to a single line like `app.at(OpenSamplePage, file_path=str(file_path)).asserts(it.IsEqualTo, "Sample page")` and the transaction `ValidateResult` does not seems to be a valid transaction the user does in the application, so this code could be merged with `SubmitText` to reduce the verbosity. However, despite these embellishments, the code works perfectly.