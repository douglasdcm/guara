# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/


from pytest import mark, raises

from guara.abstract_transaction import AbstractTransaction
from guara.policy import ExecutionPolicy
from guara.transaction import Application


class FlakyTransaction(AbstractTransaction):
    policy = ExecutionPolicy(
        abort_on_exceptions=(PermissionError,), retries_on_failure=2
    )

    def do(self, value=0):
        if value == 0:
            raise PermissionError
        else:
            raise ValueError


def test_transaction_abort_exception_if_in_list(caplog):
    with raises(PermissionError):
        Application().execute(FlakyTransaction)
    assert "aborted" in caplog.text


def test_transaction_do_not_abort_exception_if_not_in_list(caplog):
    with raises(ValueError):
        Application().execute(FlakyTransaction, value=1)
    assert "aborted" not in caplog.text


class ValidateLocal(AbstractTransaction):
    def do(self):
        pass


@mark.parametrize("value", ["invalid", ("invalid",), (object,)])
def test_transactions_returns_none_when_invalid_abort_on_exceptions(value):
    t = ValidateLocal
    t.policy = ExecutionPolicy(abort_on_exceptions=value)
    Application().execute(t)
    assert t.policy.abort_on_exceptions is None
