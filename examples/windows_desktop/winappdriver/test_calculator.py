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


class TestWindowsCalculatorWithWinAppDriver:
    def setup_method(self, method):
        """Lazy import to avoid breaking the pipeline"""
        from examples.windows_desktop.winappdriver import setup

        self._app = Application()
        self._app._driver = self.app.at(setup.OpenAppTransaction)._driver

    def teardown_method(self, method):
        """Lazy import to avoid breaking the pipeline"""
        from examples.windows_desktop.winappdriver import setup

        self._app.at(setup.CloseAppTransaction)

    @pytest.mark.parametrize("a,b,expected", [(1, 2, 3), (3, 5, 8), (0, 0, 0), (9, 1, 10)])
    def test_addition(self, a, b, expected):
        from examples.windows_desktop.winappdriver import calculator

        self._app.at(calculator.SumNumbers, num1=a, num2=b).asserts(ItShows, expected)
