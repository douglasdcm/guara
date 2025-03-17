# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

import pathlib
import random
from guara.transaction import Application
from guara import it
from examples.web_ui.splinter import setup
from examples.web_ui.splinter import home
from guara.utils import is_dry_run
from splinter import Browser


class TestSplinterIntegration:
    """
    TestSplinterIntegration is a test class for integrating Splinter with a local web page.
    Methods:
    """

    def setup_method(self, method):
        file_path = pathlib.Path(__file__).parent.parent.resolve()
        browser = None
        if not is_dry_run():
            browser = Browser("chrome", headless=True)
        self._app = Application(browser)
        self._app.at(setup.OpenSplinterApp, url=f"file:///{file_path}/sample.html")

    def teardown_method(self, method):
        self._app.at(setup.CloseSplinterApp)

    def test_local_page(self):
        text = ["cheese", "splinter", "test", "bla", "foo"]
        text = text[random.randrange(len(text))]
        self._app.at(home.SubmitTextSplinter, text=text).asserts(it.IsEqualTo, f"It works! {text}!")
        self._app.at(home.SubmitTextSplinter, text=text).asserts(it.IsNotEqualTo, "Any")
