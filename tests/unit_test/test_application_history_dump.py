from guara.abstract_transaction import AbstractTransaction
from guara.policy import ExecutionPolicy
from guara.transaction import Application


class AnyTransaction(AbstractTransaction):
    policy = ExecutionPolicy(retry_on_exceptions=(PermissionError,), pacing_time=10)

    def do(self, foo=None, foo_s=None, credit_card=None):
        print("SSSS")
        return {"foo": foo, "secret": foo_s, "card": credit_card}


def test_app_dump():
    app = (
        Application()
        .execute(AnyTransaction, foo="foo", foo_s="123qwerty")
        .execute(AnyTransaction, credit_card="oiuy")
    )
    print(app.dump_history())
    assert app.dump_history("./dump.txt") is not None


def test_app_replay():
    app = Application()

    assert app.replay("./dump.txt") is not None
