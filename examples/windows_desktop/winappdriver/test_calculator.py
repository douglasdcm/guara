from guara.transaction import Application
from examples.windows_desktop.winappdriver import setup
from examples.windows_desktop.winappdriver import calculator


class TestCalculator:
    """Test Windows Calculator using Guará + WinAppDriver"""

    def setup_method(self):
        self.app = Application()
        self.app.at(setup.OpenAppTransaction(driver=self.app._driver))

    def teardown_method(self):
        self.app.at(setup.CloseAppTransaction(driver=self.app._driver))

    def test_addition(self):
        result = self.app.at(calculator.CalculatorTransactions(), num1=5, num2=3)
        result.asserts(calculator.CalculatorTransactions().validate_result, 8)
