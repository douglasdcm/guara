from guara.transaction import AbstractTransaction  
from guara import it  


class CalculatorTransactions(AbstractTransaction):  
    """Perform calculator operations"""
    
    def do(self, num1: int, num2: int):  
        # Click number buttons and add  
        self._click_number(num1)  
        self._driver.find_element("name", "Plus").click()  
        self._click_number(num2)  
        self._driver.find_element("name", "Equals").click()  
        return self._get_result()  

    def _click_number(self, num: int):  
        """Helper to click a number button"""  
        self._driver.find_element("name", str(num)).click()  

    def _get_result(self):  
        """Extract displayed result"""  
        return self._driver.find_element(  
            "xpath", "//*[@AutomationId='CalculatorResults']"  
        ).text.replace("Display is", "").strip()  

    def validate_result(self, expected: int):  
        """Custom assertion"""  
        return it.IsEqualTo(value=str(expected))
 