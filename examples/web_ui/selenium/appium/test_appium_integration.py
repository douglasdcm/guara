import pathlib
import random
from guara.transaction import Application
from guara import it
from examples.web_ui.selenium.appium import setup
from examples.web_ui.selenium.appium import home


class TestAppiumIntegration:
    def setup_method(self, method):
        file_path = pathlib.Path(__file__).parent.parent.resolve()

        self._app = Application(None)
        self._app.at(
            setup.OpenAppiumApp,
            url=f"file:///{file_path}/sample.html",
        )

    def teardown_method(self, method):
        self._app.at(setup.CloseAppiumApp)

    def test_local_page(self):
        text = ["cheese", "appium", "test", "bla", "foo"]
        text = text[random.randrange(len(text))]
        self._app.at(home.SubmitTextAppium, text=text).asserts(
            it.IsEqualTo, f"It works! {text}!"
        )
        self._app.at(home.SubmitTextAppium, text=text).asserts(it.IsNotEqualTo, "Any")