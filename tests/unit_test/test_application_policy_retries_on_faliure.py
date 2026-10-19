# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/

from unittest.mock import patch

from pytest import raises

from guara import it
from guara.policy import ApplicationPolicy
from guara.transaction import AbstractTransaction, Application


class FlakyTransaction(AbstractTransaction):
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


def test_application_succeeds_with_no_retries():
    app = Application(execution_policy=ApplicationPolicy(retries_on_failure=3))
    app.at(FlakyTransaction, fail_until=1).asserts(it.IsEqualTo, "success")


@patch("guara.transaction.GUARA_RETRIES_ON_FAILURE", 3)
def test_application_retries_and_succeeds_before_max_retries():
    app = Application(execution_policy=ApplicationPolicy(retries_on_failure=5))
    app.at(FlakyTransaction, fail_until=3).asserts(it.IsEqualTo, "success")


@patch("guara.transaction.GUARA_RETRIES_ON_FAILURE", 1)
def test_application_retries_and_succeeds_on_last_attempt():
    app = Application(execution_policy=ApplicationPolicy(retries_on_failure=3))
    app.at(FlakyTransaction, fail_until=2).asserts(it.IsEqualTo, "success")


@patch("guara.transaction.GUARA_RETRIES_ON_FAILURE", 1)
def test_application_raises_after_max_retries():
    app = Application(execution_policy=ApplicationPolicy(retries_on_failure=1))
    with raises(Exception, match="Flaky failure!"):
        app.at(FlakyTransaction, fail_until=3)
