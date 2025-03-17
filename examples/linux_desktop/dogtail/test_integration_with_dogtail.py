# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from pytest import mark
from guara.transaction import Application
from guara.utils import is_dry_run
from examples.linux_desktop.dogtail.screens import setup
from examples.linux_desktop.dogtail.screens import calculator
from examples.linux_desktop.dogtail.assertions import this


@mark.skipif(not is_dry_run(), reason="Dry run is disabled")
class TestLinuxCalculatorWithDogtail:
    def setup_method(self, method):
        driver = None
        if not is_dry_run():
            from dogtail.tree import root
            from dogtail.procedural import run, focus

            # Dogtail first runs the app and then gets the application.
            # So the calculator is opened direclty in the fixture.
            # This is an exception when compared against with other drivers like Selenium
            # that first gets the driver and then opens the app
            app_name = "gnome-calculator"
            run(app_name)
            focus.application(app_name)
            driver = root.application("gnome-calculator")

        self._calculator = Application(driver=driver)
        self._calculator.at(
            setup.OpenApp,
        )

    def teardown_method(self, method):
        self._calculator.at(setup.CloseApp)

    @mark.parametrize("a,b,expected", [(1, 2, 3), (3, 5, 8), (0, 0, 0), (9, 1, 10)])
    def test_calculator_with_dogtail(self, a, b, expected):
        self._calculator.at(calculator.Sum, a=a, b=b).asserts(this.Shows, expected)
