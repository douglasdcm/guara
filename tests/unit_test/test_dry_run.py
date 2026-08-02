from unittest.mock import patch
from guara.transaction import Application, AbstractTransaction

class MyTransaction(AbstractTransaction):
    def do(self):
        return "success"


@patch('guara.abstract_transaction.GUARA_DRY_RUN', True)
@patch('guara.transaction.GUARA_DRY_RUN', True)
@patch('guara.assertion', True)
def test_application_is_not_executed_when_dry_run_is_true():
    app = Application()
    app.at(MyTransaction)
    assert app.result == None

def test_application_is_executed_when_dry_run_false():
    app = Application()
    app.at(MyTransaction)
    assert app.result == "success"

