from pathlib import Path
from random import randrange
from selenium import webdriver
from examples.web_ui.selenium.simple import home
from guara.transaction import Application
from guara import it
from guara import setup


class TestLocalTransaction:
    def setup_method(self, method):
        file_path = Path(__file__).parent.parent.resolve()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        self._app = Application(webdriver.Chrome(options=options))
        self._app.at(
            setup.OpenApp,
            url=f"file:///{file_path}/sample.html",
            window_width=1094,
            window_height=765,
            implicitly_wait=0.5,
        ).asserts(it.IsEqualTo, "Sample page")

    def teardown_method(self, method):
        self._app.at(setup.CloseApp)

    def test_local_page(self):
        text = ["cheese", "selenium", "test", "bla", "foo"]
        text = text[randrange(len(text))]
        self._app.at(home.SubmitText, text=text).asserts(
            it.IsEqualTo, f"It works! {text}!"
        )
        self._app.at(home.SubmitText, text=text).asserts(it.IsNotEqualTo, "Any")
