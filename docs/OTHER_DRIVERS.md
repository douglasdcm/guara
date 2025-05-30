# Using other Web Drivers

It is possible to run Guara using other Web Drivers like [Caqui](https://github.com/douglasdcm/caqui) and [Playwright](https://playwright.dev/python/docs/intro). Check the requirements of each Web Driver before execute it. For example, Playwright requires the installation of browsers separately.

```python
from pytest import fixture
from examples.web_ui.playwright.synchronous.pages import home, setup, getting_started
from guara.transaction import Application
from guara import it
from playwright.sync_api import Page


@fixture
def my_app(page: Page):
    app = Application(page)
    app.at(setup.OpenApp, with_url="https://playwright.dev/")
    yield app


def test_local_page_playwright(my_app):
    my_app.at(home.NavigateToGettingStarted).asserts(it.IsEqualTo, "Installation")
    my_app.at(getting_started.NavigateToWritingTests).asserts(it.IsNotEqualTo, "Writing Tests")
```

More examples [here](https://github.com/douglasdcm/guara/tree/main/examples)
