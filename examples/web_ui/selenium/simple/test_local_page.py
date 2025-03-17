# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from pathlib import Path
from random import randrange
from guara import it
from examples.web_ui.selenium.simple import home, setup
from guara.transaction import Application
from guara.utils import is_dry_run
from selenium import webdriver


class TestLocalPage:
    def setup_method(self, method):
        file_path = Path(__file__).parent.parent.parent.resolve()
        driver = None
        if not is_dry_run():
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            driver = webdriver.Chrome(options=options)
        self._app = Application(driver)
        self._app.at(
            setup.OpenApp,
            url=f"file:///{file_path}/sample.html",
            window_width=1094,
            window_height=765,
            implicitly_wait=0.5,
        ).asserts(it.IsEqualTo, "Sample page")

    def teardown_method(self, method):
        self._app.at(setup.CloseApp)

    def test_local_page_selenium(self):
        text = ["cheese", "selenium", "test", "bla", "foo"]
        text = text[randrange(len(text))]
        self._app.at(home.SubmitText, text=text).asserts(it.IsEqualTo, f"It works! {text}!")
        self._app.at(home.SubmitText, text=text).asserts(it.IsNotEqualTo, "Any")
