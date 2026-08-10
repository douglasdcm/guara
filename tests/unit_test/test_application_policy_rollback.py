# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/


from pytest import raises

from guara.policy import ApplicationExecutionPolicy
from guara.transaction import AbstractTransaction, Application


class MyTransaction(AbstractTransaction):
    def do(self):
        raise PermissionError()

    def undo(self):
        raise ConnectionAbortedError


def test_application_revert_all_transactions_when_rollback_enabled():
    with raises(ConnectionAbortedError):
        Application(
            execution_policy=ApplicationExecutionPolicy(rollback_on_failure=True)
        ).execute(MyTransaction)
