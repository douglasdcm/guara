# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara


from pytest import mark, raises

from guara.abstract_transaction import AbstractTransaction
from guara.transaction import Application
from guara.policy import ExecutionPolicy
class FlakyTransaction(AbstractTransaction):
    retry_on_exceptions = (PermissionError,)
    retries_on_failure = 2
    policy = ExecutionPolicy(
        retry_on_exceptions = (PermissionError,),
        retries_on_failure = 2
    )
    def do(self, value=0):
        if value==0:
            raise PermissionError
        else:
            raise ValueError


def test_transaction_retry_exception_if_in_list(caplog):
    with raises(PermissionError):
        Application().execute(FlakyTransaction)
    assert "3 / 3" in caplog.text



def test_transaction_do_not_retry_exception_if_not_in_list(caplog):
    with raises(ValueError):
        Application().execute(FlakyTransaction, value=1)
    assert "3 / 3" not in caplog.text


class ValidateLocal(AbstractTransaction):
    def do(self):
        pass

@mark.parametrize("value", ["invalid", ("invalid",), (object,)])
def test_transactions_returns_none_when_invalid_retry_on_exceptions(value):
    t = ValidateLocal
    t.policy = ExecutionPolicy(retry_on_exceptions = value)
    Application().execute(t)
    assert t.policy.retry_on_exceptions is None