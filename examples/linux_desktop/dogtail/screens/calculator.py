import logging
from guara.transaction import AbstractTransaction
from dogtail.rawinput import pressKey, keyNameAliases


class Add(AbstractTransaction):
    """
    Sums two numbers

    Args:
        a (int): The 1st number to be added
        b (int): The second number to be added

    Returns:
        the application (self._driver)
    """

    def __init__(self, driver):
        super().__init__(driver)

    def do(self, a, b):
        try:
            self._driver.child(str(a)).click()
            self._driver.child("+").click()
            self._driver.child(str(b)).click()
            pressKey(keyNameAliases.get("enter"))
        except Exception as e:
            logging.exception(f"Error while adding numbers. {str(e)}")
            raise
        return self._driver
