# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/

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

    def do(self, a, b):
        from dogtail.rawinput import keyNameAliases, pressKey

        self._driver.child(str(a)).click()
        self._driver.child("+").click()
        self._driver.child(str(b)).click()
        pressKey(keyNameAliases.get("enter"))
        return self._driver
