# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from pytest import mark
from guara.transaction import Application
from guara import it
from examples.linux_desktop.rpa_python import setup
from examples.linux_desktop.rpa_python import home
from guara.utils import is_dry_run


@mark.skipif(not is_dry_run(), reason="Dry run is disabled")
class TestRPAIntegration:
    """
    TestRPAIntegration is a test class for integrating RPA for Python with a local application.
    """

    def setup_method(self, method):

        driver = None
        if not is_dry_run():
            import rpa as r

            driver = r
        self._app = Application(driver)
        self._app.at(setup.OpenApplication, app_path="path/to/application.exe")

    def teardown_method(self, method):
        self._app.at(setup.CloseApplication)

    def test_submit_text(self):
        text = "Hello, RPA for Python!"
        self._app.at(home.SubmitTextRPA, text=text).asserts(it.IsEqualTo, text)
