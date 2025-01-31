from guara.transaction import Application  
from examples.windows_desktop.winappdriver.setup import OpenAppTransaction, CloseAppTransaction  
from examples.windows_desktop.winappdriver.calculator import CalculatorTransactions  


class TestCalculator:  
    """Test Windows Calculator using Guará + WinAppDriver"""  

    def setup_method(self):  
        self.app = Application()  
        self.app.at(OpenAppTransaction())  

    def teardown_method(self):  
        self.app.at(CloseAppTransaction())  

    def test_addition(self):  
        result = self.app.at(CalculatorTransactions(), num1=5, num2=3)  
        result.asserts(CalculatorTransactions().validate_result, 8)
