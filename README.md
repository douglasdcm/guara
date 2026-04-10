# Guará

[![PyPI Downloads](https://static.pepy.tech/badge/guara)](https://pepy.tech/projects/guara)

Guará is a Python framework for **business logic expression**.
It allows you to write production code and tests as **executable domain language**, combining:

* Business Logic Language → expresses domain behavior using Ubiquitous Language (DDD)
* Test Framework → orchestrates scenarios using Given / When / Then

Instead of focusing only on technical assertions, Guará enables you to describe **business scenarios as code**, making production code and tests readable by developers and domain experts.

## Core Idea

Guará turns code into **business narratives**:

* **Transactions** → represent actions (use cases)
* **Assertions (`it`)** → represent business expectations
* **Application DSL** → orchestrates flows in domain language

## Syntax

```python
Application.when(DoSomething [,with_parameter=value, ...]).expects(it.Matches, a_condition)
```

## Example in Action

### Modeling

```python
from guara.transaction import Application
from guara import it
from transactions import HasBalance, BuyAsset, UpdatePortfolio

def main():
    finance_app = Application()
    (
        finance_app
        .given(HasBalance)
        .when(BuyAsset, symbol="AAPL", amount=2000)
        .and_(UpdatePortfolio).expects(it.IsEqualTo, 20)
    )
```

### UI Testing

```python
from guara.transaction import Application
from guara import it
from selenium import webdriver
from transactions import OpenApp, ChangeToPortuguese, NavigateToInfoPage, CloseApp

def test_sample_web_page():
    app = Application(webdriver.Chrome())
    app.given(OpenApp, url="https://anyhost.com/")
    app.when(ChangeToPortuguese).expects(it.IsEqualTo, CONTENT_IN_PORTUGUESE)
    app.when(NavigateToInfoPage).then(it.Contains, "This project was born")
    app.execute(CloseApp)
```

## Documentation

For more information, check:
[https://guara.readthedocs.io/en/latest/](https://guara.readthedocs.io/en/latest/)
