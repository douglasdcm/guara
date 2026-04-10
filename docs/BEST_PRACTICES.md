# Best practices

## General

- (Required) Use named arguments of the transactions to keep the natural speech
```python
# do
app.at(home.Search, by_text="foo").at(home.CreateResource, named="bla")

# don't (the code will fail)
app.at(home.Search, "foo").at(home.CreateResource, "bla")
```

- Add documentation of transactions in the class level describing all arguments and the returned value.
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
- Use the `app.result` attribute to return the result of the last transaction
```python
urls = app.when(GetURLs).result
for url in urls:
    print(url)
```
- Use the `app.asserts` method directly to validate the result of the last transaction. Sometimes the user wants to get the result of the transaction to use it later.
```python
ids, data, has_more = app.when(GetArticleIDs, page=page).result
app.asserts(it.IsGreaterThan, 0)  # Verify we got articles
```
- Use the proper verb method of `app` to make the statements as natural speech
```python
app.at(home.OpenInfo, ...)
app.when(OpenInfo, ...).and_(ChangeToEnglish, ...)
```
- Use chained verb methods to build your statements in natural language
```python
app.at(home.OpenInfo, ...).and_(ChangeToEnglish, ...).asserts(...)
app.when(OpenInfo, ...).and_(ChangeToEnglish, ...).asserts(...)
app.at(home.OpenInfo, ...).at(info.ChangeToEnglish, ...).asserts(...)
```
- Give good names to parameters of transactions to keep a smooth reading
```python
# do
app.at(home.Search, by_text="foo").at(home.CreateResource, with_name="bla")

# don't
app.at(home.Search, value="foo").at(home.CreateResource, value="bla")
```
- Use named arguments in the transaction's signature
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

## Automation Testing 
- Add typing to `self._driver` in transactions to allow the autocomplete of IDEs
```python
class CloseBrowser(AbstractTransaction):
    def __init__(self, driver):
        self._driver : Chrome = driver
```
- For a better readability of the code it is recommended to use a high-level tools instead of raw Selenium commands. In this [example](https://github.com/douglasdcm/guara/tree/main/examples/web_ui/selenium/browserist) there is the complete implementation of a test using [Browserist](https://github.com/jakob-bagterp/browserist). This is one of the transactions.

```python
from browserist import Browser
from guara.transaction import AbstractTransaction


class SubmitText(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: Browser

    def do(self, text):
        TEXT = '//*[@id="input"]'
        BUTTON_TEST = '//*[@id="button"]'
        RESULT = '//*[@id="result"]'
        self._driver.input.value(TEXT, text)
        self._driver.click.button(BUTTON_TEST)
        return self._driver.get.text(RESULT)
```

- Other interesting tool is [Helium](https://github.com/mherrmann/helium). More details in this [example](https://github.com/douglasdcm/guara/tree/main/examples/web_ui/selenium/helium). Here is a transaction implementation:

```
from helium import find_all, write, click, S, Text
from guara.transaction import AbstractTransaction


class SubmitText(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)

    def do(self, text):
        TEXT = '//*[@id="input"]'
        BUTTON_TEST = "button"
        text_field = find_all(S(TEXT))[0]
        write(text, text_field)
        click(find_all(S(BUTTON_TEST))[0])
        return Text("It works!").value
```

## Advanced
For more examples of implementations check the [examples](https://github.com/douglasdcm/guara/blob/main/examples) folder.
