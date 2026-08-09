# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/

from pytest import mark
from screens import calculator, setup

from guara import it
from guara.application import Application
from guara.utils import is_dry_run


class ItShows(it.IAssertion):
    """
    It checks if the value is shown in the calculator

    Args:
        actual (application): The calculator object
        expected (number): the value that should be present in the screen
    """

    def asserts(self, actual, expected):
        assert actual.child(str(expected)).showing


@mark.skipif(not is_dry_run(), reason="Dry run is disabled")
class TestLinuxCalculatorWithPyautogui:
    def setup_method(self, method):
        driver = None
        if not is_dry_run():
            from dogtail.procedural import focus, run
            from dogtail.tree import root

            app_name = "gnome-calculator"
            run(app_name)
            focus.application(app_name)
            driver = root.application(app_name)

        self._calculator = Application(driver=driver)
        self._calculator.at(setup.OpenApp)

    def teardown_method(self, method):
        self._calculator.at(setup.CloseApp)

    def test_calculator(self):

        # Pyautogui seems not to enforce assertions. It also does not have a driver
        # which the tester could use to get information about the app. It just interacts
        # with whatever is shown in your host. One possible way to make assertions is
        # check if an specific image like `images/displays_3.png` is present in the screen
        # The tester has to be creative while asserting things with Pyautogui.
        # I'm using dogtail to return information about the opened app.
        # In this case, dogtail has to be passed as the driver to the `Application`.
        # Check the examples in `examples/linux_desktop/dogtail` for more information.
        self._calculator.at(
            calculator.Divide,
            a=1,
            b=2,
        ).asserts(ItShows, 0.5)
