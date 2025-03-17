# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from pathlib import Path
from random import randrange
from pytest import mark
from guara.transaction import Application
from guara import it
from setup import OpenAppiumApp, CloseAppiumApp
from home import SubmitTextAppium
from guara.utils import is_dry_run
from appium import webdriver


@mark.skipif(not is_dry_run(), reason="Dry run is disabled")
class TestAppiumIntegration:
    def setup_method(self, method):
        file_path = Path(__file__).resolve()
        desired_caps = {
            "platformName": "Android",
            "deviceName": "emulator-5554",
            "browserName": "Chrome",
            "app": "/absolute/path/to/sample.apk",
            "automationName": "UiAutomator2",
            "noReset": True,
            "appWaitActivity": "*",
            "goog:chromeOptions": {"args": ["--headless"]},
        }
        self.driver = None
        if not is_dry_run():
            self.driver = webdriver.Remote(
                "http://localhost:4723/wd/hub", desired_capabilities=desired_caps
            )
        self._app = Application(self.driver)
        self._app.at(OpenAppiumApp, url=f"file:///{file_path}/sample.html")

    def teardown_method(self, method):
        self._app.at(CloseAppiumApp)

    def test_local_page(self):
        text = ["cheese", "appium", "test", "bla", "foo"]
        text = text[randrange(len(text))]
        self._app.at(SubmitTextAppium, text=text).asserts(it.IsEqualTo, f"It works! {text}!")
        self._app.at(SubmitTextAppium, text=text).asserts(it.IsNotEqualTo, "Any")
