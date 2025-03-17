# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from logging import exception
from guara.transaction import AbstractTransaction


class Sum(AbstractTransaction):
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
        from dogtail.rawinput import pressKey, keyNameAliases

        if not (0 <= a <= 9) or not (0 <= b <= 9):
            raise ValueError("Inputs must be single-digit numbers between 0 and 9.")
        try:
            self._driver.child(str(a)).click()
            self._driver.child("+").click()
            self._driver.child(str(b)).click()
            pressKey(keyNameAliases.get("enter"))
        except Exception as e:
            exception(f"Error while adding numbers. {str(e)}")
            raise
        return self._driver
