import pytest
import platform
from guara.transaction import Application

# Skip the tests if not running on Windows
pytestmark = pytest.mark.skipif(
    platform.system() != "Windows", reason="WinAppDriver tests require Windows"
)


class TestCalculator:
    """Test Windows Calculator using Guará + WinAppDriver"""

    def setup_method(self):
        from examples.windows_desktop.winappdriver import setup

        self.app = Application()
        self.app.at(setup.OpenAppTransaction)

    def teardown_method(self):
        from examples.windows_desktop.winappdriver import setup

        self.app.at(setup.CloseAppTransaction)

    def test_addition(self):
        from examples.windows_desktop.winappdriver import calculator

        self.app.at(calculator.SumNumbers, num1=5, num2=3).asserts(
            calculator.SumNumbers().validate_result, 8
        )

    def test_validate_result_success(self):
        from examples.windows_desktop.winappdriver import calculator

        self.app.at(calculator.SumNumbers, num1=5, num2=3).asserts(
            calculator.SumNumbers().validate_result, 8
        )

    def test_validate_result_failure(self):
        from examples.windows_desktop.winappdriver import calculator

        self.app.at(calculator.SumNumbers, num1=5, num2=3).asserts(
            calculator.SumNumbers().validate_result, 10
        )
