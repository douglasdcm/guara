# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/guara

from unittest.mock import patch

from pytest import mark, raises

from guara import it
from guara.constants import GUARA_DRY_RUN
from guara.policy import ExecutionPolicy
from guara.transaction import AbstractTransaction, Application


# A mock transaction that fails N times before succeeding
class FlakyTransaction(AbstractTransaction):
    policy = ExecutionPolicy(return_on_dry_run=PermissionError("Flaky failure!"))

    def __init__(self, driver):
        super().__init__(driver)
        self.counter = 0

    def do(self, **kwargs):
        self.counter += 1
        if self.counter < kwargs.get("fail_until", 1):
            raise PermissionError("Flaky failure!")
        return "success"


def test_application_fails_with_no_retries():
    app = Application()
    with raises(PermissionError, match="Flaky failure!"):
        app.at(FlakyTransaction, fail_until=2)


@mark.skipif(GUARA_DRY_RUN, reason="Ignore on dry run.")
def test_application_succeeds_with_no_retries():
    app = Application()
    app.at(FlakyTransaction, fail_until=1).asserts(it.IsEqualTo, "success")


@mark.skipif(GUARA_DRY_RUN, reason="Ignore on dry run.")
@patch("guara.transaction.GUARA_RETRIES_ON_FAILURE", 3)
def test_application_retries_and_succeeds_before_max_retries():
    # Setup environment for 2 retries
    app = Application()

    # We want it to fail twice and succeed on the 2nd attempt (1st retry)
    app.at(FlakyTransaction, fail_until=3).asserts(it.IsEqualTo, "success")


@mark.skipif(GUARA_DRY_RUN, reason="Ignore on dry run.")
@patch("guara.transaction.GUARA_RETRIES_ON_FAILURE", 1)
def test_application_retries_and_succeeds_on_last_attempt():
    # Setup environment for 2 retries
    app = Application()

    # We want it to fail once and succeed on the 2nd attempt (1st retry)
    app.at(FlakyTransaction, fail_until=2).asserts(it.IsEqualTo, "success")


@patch("guara.transaction.GUARA_RETRIES_ON_FAILURE", 1)
def test_application_raises_after_max_retries():
    # Setup environment for 1 retry
    app = Application()
    # If it needs 3 attempts but we only allow 1 retry (2 attempts total), it should raise
    with raises(Exception, match="Flaky failure!"):
        app.at(FlakyTransaction, fail_until=3)


class ValidateLocalRetryRaiseException(AbstractTransaction):
    policy = ExecutionPolicy(retries_on_failure=0)

    def do(self):
        raise PermissionError("Failed!")


@mark.parametrize("value", [0, 1])
@patch("guara.transaction.GUARA_RETRIES_ON_FAILURE", 100)
def test_transaction_overrides_retries_on_failure_when_local_variable_is_positive_integer(
    value, caplog
):
    t = ValidateLocalRetryRaiseException
    t.policy = ExecutionPolicy(retries_on_failure=value)
    with raises(PermissionError):
        Application().at(t)

    assert t.policy.retries_on_failure == value

    assert "1 / 100" not in caplog.text


class ValidateLocal(AbstractTransaction):
    def do(self):
        pass


@mark.parametrize("value", ["invalid", -1, object()])
def test_transactions_returns_none_when_invalid_retry_on_failure(value):
    t = ValidateLocal
    t.policy = ExecutionPolicy(retries_on_failure=value)
    Application().execute(t)
    assert t.policy.retries_on_failure is None
