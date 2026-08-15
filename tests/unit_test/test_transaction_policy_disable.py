# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/


from pytest import mark, raises

from guara.policy import ApplicationPolicy, TransactionPolicy
from guara.transaction import AbstractTransaction, Application


class ValidateLocal(AbstractTransaction):
    def do(self):
        raise ValueError


def test_transaction_run_when_policy_disable_is_false():
    t = ValidateLocal
    t.execution_policy = TransactionPolicy(disable=False)
    with raises(ValueError):
        Application().at(t)


def test_transaction_doesnt_run_when_policy_disable_is_true(caplog):
    t = ValidateLocal
    t.execution_policy = TransactionPolicy(disable=True)
    Application().at(t)
    assert "disable" in caplog.text


def test_transaction_disable_overrides_application_disable():
    t = ValidateLocal
    t.execution_policy = TransactionPolicy(disable=True)
    Application(ApplicationPolicy(disable=False)).at(t)


@mark.parametrize("value", ["invalid", -1, object()])
def test_transactions_returns_none_when_invalid_disable_value(value):
    t = ValidateLocal
    t.execution_policy = TransactionPolicy(disable=value)
    with raises(ValueError):
        Application().execute(t)
    assert t.execution_policy.disable is None
