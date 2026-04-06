# Using ChatGPT with Page Transactions
As `Page Transactions` pattern is a new term. ChatGPT will not find a reference to it. But, it is not an excuse to not use the pattern. Teaching ChatGPT about the pattern is very easy and fast and the result is pretty much accurate.

1. Go to [ChatGPT](https://chatgpt.com/) page and login with your account. Create a new one if necessary.
3. Paste the following statements in the ChatGPT prompt
```text
Imagine you are a test automation engineer with more than 20 years of experience.
Your task is:

* Read the documentation of the test framework https://guara.readthedocs.io/en/latest/
* Explain in one paragraph what you understood about the framework
```
Here is a possible output
```text
Guará is a Python test automation framework built around the **Page Transactions** pattern,
which emphasizes modeling tests as sequences of reusable, business-level actions (transactions)
rather than page-centric structures; each transaction encapsulates the interaction logic
(e.g., UI, API, or other layers) inside a `do()` method, while a central `Application`
class orchestrates execution through a fluent interface (`at`, `then`, `asserts`) and maintains
the result state between steps, enabling clean chaining and data flow; validations are decoupled
via pluggable assertion strategies (`IAssertion`), allowing flexible and extensible verification
logic, and overall the framework promotes highly readable, maintainable, and scalable test code
that can be applied beyond UI automation, including APIs and asynchronous workflows.
```
4. Check its understanding and continue
5. Now that ChatGPT knows about the new pattern. Ask it to organize your code using this prompt
```text
Based on your understanding about the framework Guará use this framework to organize the
code CODE in a single file so that I can copy and paste it in my project

### CODE ###
<your raw code>
```
6. Check if

- `guara` is part of the imports
- `Application` is used to orchestrate the code execution with `at` and `asserts`
7. Make adjustments if necessary
8. Done! Your code is in the new pattern.

## Here is a practical example

### Raw code in Selenium

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

It is the output of ChatGPT

```python
# Here is your code fully refactored using the real Guará framework, organized in
# a single file and ready to copy & paste:


import random
import pathlib
from selenium import webdriver
from selenium.webdriver.common.by import By

from guara.transaction import AbstractTransaction, Application
from guara import it


# =========================
# Transactions
# =========================

class OpenSamplePage(AbstractTransaction):
    def do(self, file_path):
        self._driver.get(f"file:///{file_path}/sample.html")


class GetTitle(AbstractTransaction):
    def do(self):
        return self._driver.title


class FillInputWithRandomText(AbstractTransaction):
    def do(self, options):
        text_box = self._driver.find_element(By.ID, "input")
        value = random.choice(options)
        text_box.send_keys(value)
        return text_box.get_attribute("value")


class SubmitForm(AbstractTransaction):
    def do(self):
        self._driver.find_element(By.CSS_SELECTOR, "button").click()


class GetResultMessage(AbstractTransaction):
    def do(self):
        return self._driver.find_element(By.ID, "result").text


class CloseBrowser(AbstractTransaction):
    def do(self):
        self._driver.quit()


# =========================
# Test
# =========================

def test_sample_page():
    file_path = pathlib.Path(__file__).parent.resolve()
    app = Application(webdriver.Chrome())

    text_options = ["cheese", "selenium", "test", "bla", "foo"]

    # Open page
    app.at(OpenSamplePage, file_path=file_path)

    # Validate title
    app.at(GetTitle).asserts(it.IsEqualTo, "Sample page")

    # Fill input and keep value
    typed_text = app.at(
        FillInputWithRandomText,
        options=text_options
    ).result

    # Submit and validate result
    (
        app
        .at(SubmitForm)
        .at(GetResultMessage)
        .asserts(it.IsEqualTo, f"It works! {typed_text}!")
    )

    # Close browser
    app.at(CloseBrowser)
```