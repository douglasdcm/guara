from pytest import mark
import pytest
import platform
from guara.transaction import Application
from guara import it

# Skip the tests if not running on Windows
pytestmark = pytest.mark.skipif(platform.system() != "Windows", reason="Requires Windows")


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


@mark.skip(reason="Complex setup in CI environment")
class TestWindowsCalculatorWithWinAppDriver:
    """Test Windows Calculator using Guará + WinAppDriver"""

    def setup_method(self, method):
        """Lazy import to avoid breaking the pipeline"""
        from examples.windows_desktop.winappdriver import setup
        from appium import webdriver

        desired_caps = {
            "app": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
            "platformName": "Windows",
            "deviceName": "WindowsPC",
        }
        driver = webdriver.Remote(
            command_executor="http://localhost:4723/wd/hub", desired_capabilities=desired_caps
        )

        self._calculator = Application(driver=driver)
        self._calculator.at(setup.OpenAppTransaction)

    def teardown_method(self, method):
        from examples.windows_desktop.winappdriver import setup

        self._calculator.at(setup.CloseAppTransaction)

    @mark.parametrize("a,b,expected", [(1, 2, 3), (3, 5, 8), (0, 0, 0), (9, 1, 10)])
    def test_addition(self, a, b, expected):
        from examples.windows_desktop.winappdriver import calculator

        self._calculator.at(calculator.SumNumbers, num1=a, num2=b).asserts(ItShows, expected)
