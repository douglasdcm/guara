# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/


from unittest.mock import patch

from pytest import mark, raises

from guara.policy import ApplicationPolicy
from guara.transaction import AbstractTransaction, Application


class MyTransaction(AbstractTransaction):
    def do(self):
        raise PermissionError()


@mark.timeout(5)
@mark.parametrize("value", [0, 1])
@patch("guara.transaction.GUARA_PACING_TIME", 3000)
def test_application_waits_when_pacing_time_grater_than_0(value):
    with raises(PermissionError):
        Application(
            execution_policy=ApplicationPolicy(
                pacing_time=value,
                retries_on_failure=1,
            )
        ).execute(MyTransaction)


@mark.parametrize("value", ["invalid", -1, object()])
def test_application_returns_none_when_invalid_pacing_time(value):
    with raises(PermissionError):
        Application(
            execution_policy=ApplicationPolicy(
                pacing_time=value,
                retries_on_failure=1,
            )
        ).execute(MyTransaction)
