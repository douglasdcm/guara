# Copyright (C) 2025 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from random import randrange
from examples.unit_test.calculator.calculator import Calculator
from examples.unit_test.calculator import operations
from guara.transaction import Application
from guara import it


class TestCalculator:
    def setup_method(self, method):
        self._calculator = Application(Calculator())

    def test_add_returns_3_when_adding_1_and_2(self):
        text = ["cheese", "selenium", "test", "bla", "foo"]
        text = text[randrange(len(text))]
        self._calculator.at(operations.Add, a=1, b=2).asserts(it.IsEqualTo, 3)

    def test_add_returns_1_when_adding_1_to_0(self):
        text = ["cheese", "selenium", "test", "bla", "foo"]
        text = text[randrange(len(text))]
        self._calculator.at(operations.Add, a=1, b=0).asserts(it.IsEqualTo, 1)

    def test_add_returns_2_when_subtracting_1_from_2(self):
        text = ["cheese", "selenium", "test", "bla", "foo"]
        text = text[randrange(len(text))]
        self._calculator.at(operations.Subtract, a=2, b=1).asserts(it.IsEqualTo, 1)
