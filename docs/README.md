# Guará

[![PyPI Downloads](https://static.pepy.tech/badge/guara)](https://pepy.tech/projects/guara)

<img src=https://github.com/douglasdcm/guara/raw/main/docs/images/guara.jpg width="300" height="300" />

Photo by <a href="https://unsplash.com/@matcfelipe?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Mateus Campos Felipe</a> on <a href="https://unsplash.com/photos/red-flamingo-svdE4f0K4bs?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>

---

## What is Guará?

Guará is a Python framework for **business logic expression** designed to simplify production code implementation and UI test automation. Inspired by design patterns like **Page Objects**, **App Actions**, and **Screenplay**, Guará focuses on **Page Transactions**—encapsulating user interactions (transactions), such as BuyAsset, Login, Logout, or Form Submissions. It’s not just a tool; it’s a programming pattern.

### Why Guará?
- **Simplicity**: Reduces repetitive code by encapsulating interactions into reusable transactions.
- **Flexibility**: Can be extende to a specific ubiquitous language.
- **Clarity**: Makes production code and test scripts more readable and maintainable.

---

## Quick Start

### Installation
Guará requires **Python 3.8+**. Install it via pip:
```shell
pip install guara
```

### Syntax
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

### Behind the Scenes
The code is encapsulated in a transaction class:

#### Production code
```python
from guara.transaction import AbstractTransaction

class BuyAsset(AbstractTransaction):
    def do(self, symbol, amount):
        DataBase.balance -= amount
```

#### UI testing
```python
from guara.transaction import AbstractTransaction

class ChangeToPortuguese(AbstractTransaction):
    def do(self, **kwargs):
        self._driver.find_element(By.CSS_SELECTOR, "#PT-btn").click()
        return self._driver.find_element(By.CSS_SELECTOR, "#PT-label").text
```

---

## Key Features

### 1. **Page Transactions**
- Encapsulates user actions into reusable transactions.
- Reduces boilerplate code and improves readability.

### 2. **Flexible Assertions**
- Use built-in assertions like `it.IsEqualTo`, `it.Contains`, and more to validate outcomes.

### 3. **Cross-Driver Compatibility**
- Works with Selenium and can be adapted to other web drivers.

### 4. **Asynchronous Execution**
- Supports asynchronous operations for modern web applications.

### 5. **ChatGPT Assistance**
- Leverage AI to generate or debug transactions.

---
### Complete Tutorial
[![Watch the video](https://github.com/douglasdcm/guara/blob/main/docs/images/guara-demo.png?raw=true)](https://www.youtube.com/watch?v=Cz1k2d8Dbgc&list=PLR5jeODwvciLaJErpM4PNXnKvLRe9Hc53)

### Examples
Explore practical examples in the [examples folder](https://github.com/douglasdcm/guara/tree/main/examples).

## Contributing

### How You Can Help
- **Star this project** on GitHub.
- **Share** it with your network.
- **Write** a blog post or tutorial about Guará.
- **Contribute code**: Check out the [good first issues](https://github.com/douglasdcm/guara/issues) and submit a pull request.

---

## Why the Name "Guará"?
Guará is the Tupi–Guarani name for the **Scarlet Ibis**, a vibrant bird native to South America. Just like the bird, Guará stands out for its simplicity and elegance in solving complex UI automation challenges.

---
## Used by

- [@cu-sanjay/cricket-score-scraper](https://github.com/cu-sanjay/cricket-score-scraper)
- [@theijhay/platform_automation](https://github.com/theijhay/platform_automation)
- [@srmorita/py-selenium-practices](https://github.com/srmorita/py-selenium-practices)
- [@douglasdcm/automacao_de_testes](https://github.com/douglasdcm/automacao_de_testes)
- [@chalakbilla/React-tutorials](https://github.com/chalakbilla/React-tutorials)
- [@chriskyfung/InstapaperScraper](https://github.com/chriskyfung/InstapaperScraper)


## Ready to Dive In?
Start automating with Guará today! Check out the tutorial and explore the [examples](https://github.com/douglasdcm/guara/tree/main/examples) to see how Guará can simplify your UI testing workflow.

---

**Guará**: Simplifying UI automation, one transaction at a time. 🚀
