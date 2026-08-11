# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/


from typing import ClassVar

from pytest import mark, raises

from guara.transaction import AbstractTransaction, Application


class ValidateLocal(AbstractTransaction):
    # Must set the method name as string to avoid 'undefined' method error
    postconditions: ClassVar = [("ensure_connection_open", {"connection": "sqlite"})]

    def do(self):
        pass

    def ensure_connection_open(self, connection):
        raise ConnectionError(f"{connection} failed")


def test_transaction_run_postconditions_when_postconditions_configured():
    with raises(ConnectionError):
        Application().at(ValidateLocal)


def standalone_poscondition(connection):
    raise ConnectionAbortedError


def test_transaction_run_postconditions_when_postconditions_outside_transaction():
    t = ValidateLocal
    t.postconditions = [(standalone_poscondition, {"connection": "sqlite"})]
    with raises(ConnectionAbortedError):
        Application().at(ValidateLocal)


def simple_poscondition():
    raise PermissionError


def test_transaction_poscondition_overrides_application_postconditions():
    with raises(ConnectionError):
        Application(postconditions=[(simple_poscondition,)]).at(ValidateLocal)


@mark.parametrize("value", ["invalid", -1, object(), ("func", 0), (0, {"0": 0})])
def test_transaction_postconditions_fails_when_invalid_postconditions(value):
    t = ValidateLocal
    with raises((ValueError, TypeError)):
        t.postconditions = value
        Application().at(t)
