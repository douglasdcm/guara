# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/


from typing import ClassVar

from pytest import mark, raises

from guara.transaction import AbstractTransaction, Application


class ValidateLocal(AbstractTransaction):
    # Must set the method name as string to avoid 'undefined' method error
    preconditions: ClassVar = [("ensure_connection_open", {"connection": "sqlite"})]

    def do(self):
        raise ValueError

    def ensure_connection_open(self, connection):
        raise ConnectionError(f"{connection} failed")


def test_transaction_run_preconditions_when_preconditions_configured():
    with raises(ConnectionError):
        Application().at(ValidateLocal)


def standalone_precondition(connection):
    raise ConnectionAbortedError


def test_transaction_run_preconditions_when_preconditions_outside_transaction():
    t = ValidateLocal
    t.preconditions = [(standalone_precondition, {"connection": "sqlite"})]
    with raises(ConnectionAbortedError):
        Application().at(ValidateLocal)


def simple_precondition():
    raise PermissionError


def test_transaction_precondition_overrides_application_preconditions():
    with raises(ConnectionError):
        Application(preconditions=[(simple_precondition,)]).at(ValidateLocal)


@mark.parametrize("value", ["invalid", -1, object(), ("func", 0), (0, {"0": 0})])
def test_transaction_preconditions_fails_when_invalid_preconditions(value):
    t = ValidateLocal
    with raises((ValueError, TypeError)):
        t.preconditions = value
        Application().at(t)
