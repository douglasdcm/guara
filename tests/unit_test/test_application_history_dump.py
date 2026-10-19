from dataclasses import dataclass

from guara.abstract_transaction import AbstractTransaction
from guara.policy import TransactionPolicy
from guara.transaction import Application

DUMP_FILE = "./dump.json"


class AnyTransaction(AbstractTransaction):
    execution_policy = TransactionPolicy(
        retry_on_exceptions=(PermissionError,), pacing_time=10
    )

    def do(self, foo=None, foo_s=None, credit_card=None):
        return {"foo": foo, "secret": foo_s, "card": credit_card}


def test_app_dump():
    app = (
        Application()
        .execute(AnyTransaction, foo="foo", foo_s="123qwerty")
        .execute(AnyTransaction, credit_card="oiuy")
    )
    assert app.dump_history(DUMP_FILE) is not None

@dataclass
class EntityWithSensitiveData:
    password : str = "foo123"
    secret :str = "bla123"

    def __repr__(self):
        return f"{self.__class__.__name__}(password='***', secret='***')"

def test_app_dump_hide_sentivive_data():
    app = (
        Application()
        .execute(AnyTransaction, foo=EntityWithSensitiveData())
    )
    actual = app.dump_history()
    assert "password" in actual
    assert "secret" in actual
    assert "foo123" not in actual
    assert "bla123" not in actual


def test_app_replay():
    app = Application()
    assert app.replay(DUMP_FILE) is not None
