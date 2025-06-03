- `AbstractTransaction`: This is the class from which all transactions inherit. The `do` method is implemented by each transaction. In this method, calls to WebDriver are placed. If the method returns something, like a string, the automation can use it for assertions.
- `OpenApp` and `CloseApp` are examples of concrete transactions.
- `IAssertion`: This is the interface implemented by all concrete assertions.
- The `asserts` method of each concrete assertion contains the logic to perform validations. For example, the `IsEqualTo` concrete assertion compares the `result` with the expected value provided by the tester.
- Testers can inherit from this interface to add new sub-classes of validations that the framework does not natively support.
- `Application`: This is the runner of the automation. It executes the `do` method of each transaction and validates the result using the `asserts` method.
- The `asserts` method receives a reference to an `IAssertion` instance. It implements the `Strategy Pattern (GoF)` to allow its behavior to change at runtime.
- Another important component of the `Application` is the `result` property. It holds the result of the transaction, which can be used by `asserts` or inspected by the test using the native built-in `assert` method.
The idea is to group blocks of interactions into classes. These classes inherit from `AbstractTransaction` and override the `do` method.
Each transaction is passed to the `Application` instance, which provides the methods `at` and `asserts`. These are the only two methods necessary to orchestrate the automation. While it is primarily bound to `Selenium WebDriver`, experience shows that it can also be used to test REST APIs, unit tests and can be executed in asynchronous mode.
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
1. Add typing to `self._driver` in transactions to allow the autocomplete of IDEs
```python
class CloseBrowser(AbstractTransaction):
    def __init__(self, driver):
        self._driver : Chrome = driver
```
2. Add documentation of transactions in the class level describing all arguments and the returned value.
```python
class SaveFlightData(AbstractTransaction):
    """
    Saves flight data to a JSON file after filtering outdated data.

    Args:
        flights_data (list): The list of flight data to save.
        history_days (int): The number of days to retain in history.

    Returns:
        str: A message indicating the data was saved.
    """
    def do(self, flights_data, history_days):
        existing_data = read_json_file("flights_data.json", [])
        current_date = datetime.now().date()
```
3. Use the `app.result` attribute to return the result of the last transaction
```python
urls = app.at(GetURLs).result
for url in urls:
    print(url)
```
4. Use the `app.asserts` method directly to validate the result of the last transaction. Sometimes the user wants to get the result of the transaction to use it later.
```python
ids, data, has_more = app.at(GetArticleIDs, page=page).result
app.asserts(it.IsEqualTo, len(ids) > 0, True)  # Verify we got articles
```
5. Use the proper verb method of `app` to make the statements as natural speech
```python
app.at(home.OpenInfo, ...)
app.when(OpenInfo, ...).then(ChangeToEnglish, ...)
```
6. Use chained verb methods to build your statements in natural language
```python
app.at(home.OpenInfo, ...).then(ChangeToEnglish, ...).asserts(...)
app.when(OpenInfo, ...).then(ChangeToEnglish, ...).asserts(...)
app.at(home.OpenInfo, ...).at(info.ChangeToEnglish, ...).asserts(...)
```
7. Give good names to parameters of transactions to keep a smooth reading
```python
# do
app.at(home.Search, by_text="foo").at(home.CreateResource, with_name="bla")

# don't
app.at(home.Search, value="foo").at(home.CreateResource, value="bla")
```
8. (Required) Use named arguments of the transactions to keep the natural speech
```python
# do
app.at(home.Search, by_text="foo").at(home.CreateResource, named="bla")

# don't (the code will fail)
app.at(home.Search, "foo").at(home.CreateResource, "bla")
```
9. Use named arguments in the transaction's signature
```python
# recommended
class SaveFlightData(AbstractTransaction):
    def do(self, flights_data, history_days):
        existing_data = read_json_file(flights_data)
        current_date = timedelta(days=history_days)

# not recommended
class SaveFlightData(AbstractTransaction):
    def do(self, **kwargs):
        existing_data = read_json_file(kwargs.get(flights_data))
        current_date = timedelta(days=kwargs.get(history_days))
```

