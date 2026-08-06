# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

import pathlib

from splinter import Browser

from examples.web_ui.splinter import home, setup
from guara import it
from guara.application import Application
from guara.utils import is_dry_run


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
        text = "guara"
        self._app.at(home.SubmitTextSplinter, text=text).asserts(it.IsEqualTo, f"It works! {text}!")
        self._app.at(home.SubmitTextSplinter, text=text).asserts(it.IsNotEqualTo, "Any")
