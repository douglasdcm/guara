import random
from calculator import Calculator
from tests.unit_test import calculator_transactions
from guara.transaction import Application
from guara import it


class TestCalculator:
    def setup_method(self, method):
        self._app = Application(Calculator)

    def test_add_return_3_when_add_1_to_2(self):
        text = ["cheese", "selenium", "test", "bla", "foo"]
        text = text[random.randrange(len(text))]

        self._app.at(calculator_transactions.Add, a=1, b=2).asserts(it.IsEqualTo, 3)

    def test_add_return_1_when_add_1_to_0(self):
        text = ["cheese", "selenium", "test", "bla", "foo"]
        text = text[random.randrange(len(text))]

        self._app.at(calculator_transactions.Add, a=1, b=0).asserts(it.IsEqualTo, 1)

    def test_add_return_2_when_subtract_1_from_2(self):
        text = ["cheese", "selenium", "test", "bla", "foo"]
        text = text[random.randrange(len(text))]

        self._app.at(calculator_transactions.Subtract, a=2, b=1).asserts(
            it.IsEqualTo, 1
        )
