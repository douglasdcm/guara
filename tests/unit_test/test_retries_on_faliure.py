from unittest.mock import MagicMock, patch
from guara.transaction import Application, AbstractTransaction
import os
from pytest import raises
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

def test_application_retries_and_succeeds():
    # Setup environment for 2 retries
    with patch.dict(os.environ, {"RETRIES_ON_FAILURE": "2"}):
        app = Application(driver=MagicMock())
        
        # We want it to fail once and succeed on the 2nd attempt (1st retry)
        app.at(FlakyTransaction, fail_until=2)
        
        assert app.result == "success"

def test_application_raises_after_max_retries():
    # Setup environment for 1 retry
    with patch.dict(os.environ, {"RETRIES_ON_FAILURE": "1"}):
        app = Application(driver=MagicMock())
        
        # If it needs 3 attempts but we only allow 1 retry (2 attempts total), it should raise
        with raises(Exception) as excinfo:
            app.at(FlakyTransaction, fail_until=3)
        
        assert "Flaky failure!" in str(excinfo.value)