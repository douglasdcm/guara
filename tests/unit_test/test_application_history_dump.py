from guara.abstract_transaction import AbstractTransaction
from guara.transaction import Application


class AnyTransaction(AbstractTransaction):
    def do(self, foo=None, foo_s=None, credit_card=None):
        return {"foo": foo, "secret": foo_s, "card": credit_card}


def test_app_dump():
    app = (
        Application()
        .execute(AnyTransaction, foo="foo", foo_s="123qwerty")
        .execute(AnyTransaction, credit_card="oiuy")
    )

    assert app.dump_history("./dump.txt") is not None


def test_app_replay():
    app = Application()

    assert app.replay("./dump.txt") is not None
