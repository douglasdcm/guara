# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from unittest.mock import patch

from pytest import mark, raises

from guara.policy import ExecutionPolicy
from guara.transaction import AbstractTransaction, Application


class ValidateLocal(AbstractTransaction):
    policy = ExecutionPolicy(
        retries_on_failure=1
    )
    def do(self):
        raise ValueError

@mark.timeout(5 )
@mark.parametrize("value", [0, 1])
@patch("guara.transaction.GUARA_PACING_TIME", 3000)
def test_transaction_overrides_pacing_time_when_local_variable_is_positive_integer(value):
    t = ValidateLocal
    t.policy = ExecutionPolicy(pacing_time = value)
    with raises(ValueError):
        Application().at(t)
    assert t.policy.pacing_time == value


@mark.parametrize("value", ["invalid", -1, object()])
def test_transactions_returns_none_when_invalid_pacing_time(value):
    t = ValidateLocal
    t.policy = ExecutionPolicy(pacing_time = value)
    with raises(ValueError):
        Application().execute(t)
    assert t.policy.pacing_time is None