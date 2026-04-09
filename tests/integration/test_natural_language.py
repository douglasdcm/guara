from guara.transaction import Application, AbstractTransaction
from guara import it

# ===================
# Use natual language
# ===================


class UserLoggedIn(AbstractTransaction):
    def do(self):
        pass


class Search(AbstractTransaction):
    def do(self, **kwargs):
        pass


class SelectItem(AbstractTransaction):
    def do(self):
        pass


class ReportChart(AbstractTransaction):
    def do(self):
        return 1


def test_natural_laguage():
    app = Application()
    (
        app.given(UserLoggedIn)
        .when(Search, product="notebook")
        .and_(SelectItem)
        .and_(ReportChart)
        .then(it.IsEqualTo, 1)
    )


# ===============
# Extend language
# ===============


class FinancialApplication(Application):
    def __init__(self, driver=None):
        super().__init__(driver)

    # GIVEN block
    def account_with(self, transaction, **kwargs):
        super().given(transaction, **kwargs)
        return self

    def portfolio_with(self, transaction, **kwargs):
        super().given(transaction, **kwargs)
        return self

    def positioned_with(self, transaction, **kwargs):
        super().given(transaction, **kwargs)
        return self

    # WHEN block
    def execute(self, transaction, **kwargs):
        super().when(transaction, **kwargs)
        return self

    def trade(self, transaction, **kwargs):
        super().when(transaction, **kwargs)
        return self

    def process(self, transaction, **kwargs):
        super().when(transaction, **kwargs)
        return self

    def settles(self, transaction, **kwargs):
        super().when(transaction, **kwargs)
        return self

    # THEN block
    def result_in(self, transaction, **kwargs):
        super().then(transaction, **kwargs)
        return self

    def update(self, transaction, **kwargs):
        super().then(transaction, **kwargs)
        return self

    def reconciles(self, assertion, expected):
        super().asserts(assertion, expected)
        return self

    def balances(self, assertion, expected):
        super().asserts(assertion, expected)
        return self

    def complies(self, assertion, expected):
        super().asserts(assertion, expected)
        return self

    def validates(self, assertion, expected):
        super().asserts(assertion, expected)
        return self


class DataBase:
    balance = 200000
    portifolio = 1234


# Transations
class HasBalance(AbstractTransaction):
    def do(self):
        assert DataBase.balance > 0


class BuyAsset(AbstractTransaction):
    def do(self, symbol, amount):
        DataBase.balance -= amount


class UpdatePortfolio(AbstractTransaction):
    def do(self):
        balance = DataBase.balance
        DataBase.portifolio = round(balance / 10000)
        return DataBase.portifolio


# Assertions
class ExpectedPortfolio(it.IsEqualTo):
    def __init__(self):
        super().__init__()


class ExpectedLedger(it.IsEqualTo):
    def __init__(self):
        super().__init__()


def test_extend_ubiquitous_language():
    fin_app = FinancialApplication()
    (
        fin_app.account_with(HasBalance)
        .execute(BuyAsset, symbol="AAPL", amount=2000)
        .settles(UpdatePortfolio)
        .reconciles(ExpectedPortfolio, 20)
    )
