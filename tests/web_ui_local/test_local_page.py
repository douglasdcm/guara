import pathlib
import random
from selenium import webdriver
from tests.web_ui_local import home
from guara.transaction import Application
from guara import it
from guara import setup


class TestLocalTransaction:
    def setup_method(self, method):
        file_path = pathlib.Path(__file__).parent.resolve()

        self._app = Application(webdriver.Chrome())
        self._app.at(
            setup.OpenApp,
            url=f"file:///{file_path}/sample.html",
            window_width=1094,
            window_hight=765,
            implicitly_wait=0.5,
        )

    def teardown_method(self, method):
        self._app.at(setup.CloseApp)

    def test_vpm_transaction_chain(self):
        text = ["cheese", "selenium", "test", "bla", "foo"]
        text = text[random.randrange(len(text))]
        self._app.at(home.SubmitText, text=text).asserts(
            it.IsEqualTo, f"It works! {text}!"
        )
        self._app.at(home.SubmitText, text=text).asserts(it.IsNotEqualTo, "Any")
