# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/


from guara import it
from guara.transaction import AbstractTransaction, Application


class MyTransaction(AbstractTransaction):
    def do(self, secret):
        return secret


def test_dump_does_not_expose_secrets():
    secret = "123qwerty"
    app = Application()
    result = (
        app.given(MyTransaction, secret=secret)
        .at(MyTransaction, secret=secret)
        .asserts(it.IsEqualTo, secret)
        .dump_history()
    )

    assert secret not in result


class MyOtherTransaction(AbstractTransaction):
    def do(self, param1, param2):
        return (param1, param2)


def test_replay_dump(caplog):
    app = Application()
    (
        app.given(MyOtherTransaction, param1="param1", param2="param2")
        .at(MyOtherTransaction, param1="param1", param2="param2")
        .asserts(it.IsNotNone)
    )

    Application().replay(app.history)
    assert "Replaying transaction" in caplog.text
