# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from pytest import mark
from guara.transaction import Application
from guara import it
from guara.utils import is_dry_run
from examples.windows_desktop.pyautowin import setup, home


@mark.skipif(not is_dry_run(), reason="Dry run is disabled")
class TestPyAutoWinIntegration:
    """
    TestPyAutoWinIntegration is a test class for integrating PyAutoWin with a local application.
    """

    def setup_method(self, method):
        driver = None
        if not is_dry_run():
            # Lazy import as PyAutoWin needs Windows OS resources
            import pyautowin

            driver = pyautowin
        self._app = Application(driver)
        self._app.at(setup.OpenApplication, app_path="path/to/application.exe")

    def teardown_method(self, method):
        self._app.at(setup.CloseApplication, app_name="Application Name")

    def test_submit_text(self):
        text = "Hello, PyAutoWin!"
        self._app.at(home.SubmitTextPyAutoWin, text=text).asserts(it.IsEqualTo, text)
