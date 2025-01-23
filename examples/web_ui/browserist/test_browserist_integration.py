from pathlib import Path
from random import randrange
from guara.transaction import Application
from guara import it
from examples.web_ui.browserist import setup
from examples.web_ui.browserist import home
from browserist import Browser, BrowserSettings


class TestBrowseristIntegration:
    def setup_method(self, method):
        file_path = Path(__file__).parent.parent.resolve()

        self._app = Application(Browser(BrowserSettings(headless=True)))
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
