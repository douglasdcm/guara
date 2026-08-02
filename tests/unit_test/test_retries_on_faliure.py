from unittest.mock import patch
from guara.transaction import Application, AbstractTransaction
from pytest import raises, mark

from guara.utils import get_retries_on_failure


# A mock transaction that fails N times before succeeding
class FlakyTransaction(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)
        self.counter = 0

    def do(self, **kwargs):
        self.counter += 1
        if self.counter < kwargs.get("fail_until", 1):
            raise Exception("Flaky failure!")
        return "success"


def test_application_fails_with_no_retries():
    app = Application()
    with raises(Exception) as excinfo:
        app.at(FlakyTransaction, fail_until=2)

        assert "Flaky failure!" in str(excinfo.value)


def test_application_succeeds_with_no_retries():
    app = Application()
    app.at(FlakyTransaction, fail_until=1)
    assert app.result == "success"


def test_application_retries_and_succeeds_before_max_retries():
    # Setup environment for 2 retries
    with patch("guara.transaction.get_retries_on_failure", return_value=2):
        app = Application()

        # We want it to fail once and succeed on the 2nd attempt (1st retry)
        app.at(FlakyTransaction, fail_until=2)

        assert app.result == "success"


def test_application_retries_and_succeeds_on_last_attempt():
    # Setup environment for 2 retries
    with patch("guara.transaction.get_retries_on_failure", return_value=1):
        app = Application()

        # We want it to fail once and succeed on the 2nd attempt (1st retry)
        app.at(FlakyTransaction, fail_until=2)

        assert app.result == "success"


def test_application_raises_after_max_retries():
    # Setup environment for 1 retry
    with patch("guara.transaction.get_retries_on_failure", return_value=1):
        app = Application()
        # If it needs 3 attempts but we only allow 1 retry (2 attempts total), it should raise
        with raises(Exception) as excinfo:
            app.at(FlakyTransaction, fail_until=3)

        assert "Flaky failure!" in str(excinfo.value)




@mark.parametrize("value,expected", [(-1,0), (0,0), (1, 1)])
def test_get_retries_on_return_correct_value(value, expected):
    assert get_retries_on_failure(value) == expected