# Guará
[![PyPI Downloads](https://static.pepy.tech/badge/guara)](https://pepy.tech/projects/guara)

Guará is a Python framework designed to simplify UI test automation.

### Syntax
```python
Application.at(apage.DoSomething [,with_parameter=value, ...]).asserts(it.Matches, a_condition)
```

### Example in Action
```python
from selenium import webdriver
from pages import home, contact, info, setup
from guara.transaction import Application
from guara import it

def test_sample_web_page():
    # Initialize the Application with a driver
    app = Application(webdriver.Chrome())
    # Open the web application
    app.at(setup.OpenApp, url="https://anyhost.com/")
    # Change language to Portuguese and assert content
    app.at(home.ChangeToPortuguese).asserts(it.IsEqualTo, content_in_portuguese)
    # Navigate to Info page and assert text presence
    app.at(info.NavigateTo).asserts(it.Contains, "This project was born")
    # Close the web application
    app.at(setup.CloseApp)
```

For more information, check [the documentation](https://guara.readthedocs.io/en/latest/)
