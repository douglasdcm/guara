from guara.transaction import AbstractTransaction
import logging


class SumNumbers(AbstractTransaction):
    """Perform addition operation"""

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, num1: int, num2: int):
        try:
            logging.info(f"Performing addition: {num1} + {num2}")
            self._click_number(num1)
            self._driver.find_element("name", "Plus").click()
            self._click_number(num2)
            self._driver.find_element("name", "Equals").click()
            result = self._get_result()
            logging.info(f"Result: {result}")
            return result
        except Exception as e:
            logging.error(f"Error performing addition: {e}")
            raise

    def _click_number(self, num: int):
        """Helper to click a number button"""
        try:
            logging.info(f"Clicking number: {num}")
            self._driver.find_element("name", str(num)).click()
        except Exception as e:
            logging.error(f"Error clicking number {num}: {e}")
            raise

    def _get_result(self):
        """Extract displayed result"""
        try:
            result = (
                self._driver.find_element("xpath", "//*[@AutomationId='CalculatorResults']")
                .text.replace("Display is", "")
                .strip()
            )
            logging.info(f"Extracted result: {result}")
            return result
        except Exception as e:
            logging.error(f"Error extracting result: {e}")
            raise
