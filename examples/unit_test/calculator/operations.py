# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from guara.transaction import AbstractTransaction
from examples.unit_test.calculator.calculator import Calculator


class Add(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: Calculator

    def do(self, a, b):
        return self._driver.add(a, b)


class Subtract(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self._driver: Calculator

    def do(self, a, b):
        return self._driver.subtract(a, b)
