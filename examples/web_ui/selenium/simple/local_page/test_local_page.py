"""
The testing module that allows the testing of Selenium on
local pages.
"""

from pathlib import Path
from random import randrange
from guara.transaction import Application
from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.chrome.options import Options
from guara.setup import OpenApp, CloseApp
from guara.it import IsEqualTo, IsNotEqualTo
from typing import List
from examples.web_ui.selenium.simple.local_page import home


class TestLocalPage:
    def setup_method(self) -> None:
        file_path: Path = Path(
            __file__
        ).parent.parent.parent.parent.resolve()
        options: Options = ChromeOptions()
        options.add_argument("--headless=new")
        self._app: Application = Application(
            Chrome(options=options)
        )
        self._app.at(
            transaction=OpenApp,
            url=f"file:///{file_path}/sample.html",
            window_width=1094,
            window_height=765,
            delay=0.5,
        ).asserts(IsEqualTo, "Sample page")

    def teardown_method(self) -> None:
        self._app.at(CloseApp)

    def test_local_page(self):
        text = ["cheese", "selenium", "test", "bla", "foo"]
        text = text[randrange(len(text))]
        self._app.at(home.SubmitText, text=text).asserts(IsEqualTo, f"It works! {text}!")
        self._app.at(home.SubmitText, text=text).asserts(IsNotEqualTo, "Any")
