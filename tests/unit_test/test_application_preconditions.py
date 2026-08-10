# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/


from pytest import mark, raises

from guara.abstract_transaction import AbstractTransaction
from guara.transaction import Application, PreconditionError


def ensure_database_connection(connection):
    pass


def ensure_api_connection(connection):
    raise ConnectionAbortedError(f"{connection} failed")


class MyTransaction(AbstractTransaction):
    def do(self):
        raise UnicodeDecodeError


def test_application_runs_precontions_before_transactions():
    with raises(ConnectionAbortedError, match="http failed"):
        Application(
            preconditions=[
                (ensure_database_connection, {"connection": "sqlite"}),
                (ensure_api_connection, {"connection": "http"}),
            ]
        ).execute(MyTransaction)


@mark.parametrize("value", ["invalid", ("invalid",), (object, "invalid")])
def test_application_fails_when_invalid_precontions(value):
    with raises(PreconditionError):
        Application(preconditions=[value]).execute(MyTransaction)
