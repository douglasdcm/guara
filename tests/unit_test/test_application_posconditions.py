# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/


from pytest import mark, raises

from guara.abstract_transaction import AbstractTransaction
from guara.transaction import Application, PosconditionError


def ensure_database_connection_closed(connection):
    pass


def ensure_api_connection_closed(connection):
    raise ConnectionAbortedError(f"{connection} failed")


class MyTransaction(AbstractTransaction):
    def do(self):
        pass


def test_application_runs_poscontions_before_transactions():
    with raises(ConnectionAbortedError, match="http failed"):
        Application(
            posconditions=[
                (ensure_database_connection_closed, {"connection": "sqlite"}),
                (ensure_api_connection_closed, {"connection": "http"}),
            ]
        ).execute(MyTransaction)


@mark.parametrize("value", ["invalid", ("invalid",), (object, "invalid")])
def test_application_fails_when_invalid_poscontions(value):
    with raises(PosconditionError):
        Application(posconditions=[value]).execute(MyTransaction)
