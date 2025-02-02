from guara.transaction import Application
from examples.windows_desktop.winappdriver import setup
from examples.windows_desktop.winappdriver import calculator
import pytest


class TestCalculator:
    """Test Windows Calculator using Guará + WinAppDriver"""

    def setup_method(self):
        self.app = Application()
        self.app._driver = self.app.at(setup.OpenAppTransaction())._driver

    def teardown_method(self):
        self.app.at(setup.CloseAppTransaction(driver=self.app._driver))

    def test_addition(self):
        self.app.at(calculator.CalculatorTransactions, num1=5, num2=3).asserts(
            calculator.CalculatorTransactions().validate_result, 8
        )

    def test_validate_result_success(self):
        self.app.at(calculator.CalculatorTransactions, num1=5, num2=3).asserts(
            calculator.CalculatorTransactions().validate_result, 8
        )

    def test_validate_result_failure(self):
        self.app.at(calculator.CalculatorTransactions, num1=5, num2=3).asserts(
            calculator.CalculatorTransactions().validate_result, 10
        )
