import pathlib
import random
from appium import webdriver
from appium.options.android import UiAutomator2Options
from guara.transaction import Application
from guara import it
from setup import OpenAppiumApp, CloseAppiumApp
from home import SubmitTextAppium

class TestAppiumIntegration:
    def setup_method(self, method):
        file_path = pathlib.Path(__file__).parent.resolve()

        """UiAutomator2Options for modern capabilities setup"""
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "emulator-5554"
        options.browser_name = "Chrome"
        options.app = "/absolute/path/to/sample.apk"
        options.automation_name = "UiAutomator2"
        options.no_reset = True
        options.app_wait_activity = "*"
        options.chrome_options = {'args': ['--headless']}

        """Options object instead of desired_capabilities"""
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
        self._app = Application(self.driver)
        self._app.at(OpenAppiumApp, url=f"file:///{file_path}/sample.html")

    def teardown_method(self, method):
        self._app.at(CloseAppiumApp)

    def test_local_page(self):
        text = ["cheese", "appium", "test", "bla", "foo"]
        text = text[random.randrange(len(text))]
        self._app.at(SubmitTextAppium, text=text).asserts(
            it.IsEqualTo, f"It works! {text}!"
        )
        self._app.at(SubmitTextAppium, text=text).asserts(it.IsNotEqualTo, "Any")
