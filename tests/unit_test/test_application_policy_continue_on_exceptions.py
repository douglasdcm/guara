# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/


from pytest import mark, raises

from guara.abstract_transaction import AbstractTransaction
from guara.policy import TransactionPolicy
from guara.transaction import Application


class FlakyTransaction(AbstractTransaction):
    def do(self, value=0):
        if value == 0:
            raise PermissionError
        else:
            raise ValueError


def test_application_continue_exception_if_in_list(caplog):
    Application(
        execution_policy=TransactionPolicy(
            continue_on_exceptions=(PermissionError,), retries_on_failure=2
        )
    ).execute(FlakyTransaction)
    assert "continued" in caplog.text


def test_application_do_not_continue_exception_if_not_in_list(caplog):
    with raises(ValueError):
        Application(
            execution_policy=TransactionPolicy(
                continue_on_exceptions=(PermissionError,), retries_on_failure=2
            )
        ).execute(FlakyTransaction, value=1)
    assert "continued" not in caplog.text


class ValidateLocal(AbstractTransaction):
    def do(self):
        pass


@mark.parametrize("value", ["invalid", ("invalid",), (object,)])
def test_applications_returns_none_when_invalid_continue_on_exceptions(value):
    app = Application(
        execution_policy=TransactionPolicy(
            continue_on_exceptions=value, retries_on_failure=2
        )
    )
    app.execute(ValidateLocal)
    assert app._policy.continue_on_exceptions is None
