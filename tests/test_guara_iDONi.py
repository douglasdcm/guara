from guara.transaction import Application, AbstractTransaction
from guara import it
from guara.setup import OpenApp, CloseApp
from selenium import webdriver


class Demo(AbstractTransaction):
    def do(self, **kwargs):
        return self._driver.current_url


def test_demo_idons():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    app = Application(webdriver.Chrome(options=options))
    app.when(OpenApp, url="https://example.com/").asserts(it.IsEqualTo, "Example Domain")
    app.when(Demo).asserts(it.IsEqualTo, "https://example.com/")
    app.at(CloseApp)
