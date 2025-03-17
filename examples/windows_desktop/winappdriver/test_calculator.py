import pytest
from guara.transaction import Application
from guara import it
from guara.utils import is_dry_run
from examples.windows_desktop.winappdriver import setup, calculator

if not is_dry_run():
    from appium import webdriver
    from appium.options.windows import WindowsOptions


class ItShows(it.IAssertion):
    """
    It checks if the value is shown in the calculator

    Args:
        actual (application): The calculator object
        expected (number): the value that should be present in the screen
    """

    def __init__(self):
        super().__init__()

    def asserts(self, actual, expected):
        assert actual.child(str(expected)).showing


class TestWindowsCalculatorWithWinAppDriver:
    def setup_method(self, method):
        driver = None
        if not is_dry_run():
            options = WindowsOptions()
            options.set_capability("app", "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App")
            options.set_capability("platformName", "Windows")
            options.set_capability("deviceName", "WindowsPC")
            driver = webdriver.Remote(
                command_executor="http://localhost:4723/wd/hub", options=options
            )
        self._app = Application(driver)

    def teardown_method(self, method):
        self._app.at(setup.CloseAppTransaction)

    @pytest.mark.parametrize("a,b,expected", [(1, 2, 3), (3, 5, 8), (0, 0, 0), (9, 1, 10)])
    def test_addition(self, a, b, expected):

        self._app.at(calculator.SumNumbers, num1=a, num2=b).asserts(ItShows, expected)
