from datetime import datetime, timezone
from typing import ClassVar

from bakery.backend.constants import SESSION_FILE
from bakery.backend.contracts import EntityIsNotNone
from bakery.backend.entities import User
from bakery.backend.exceptions import (
    BusinessError,
    CashAlreadyClosed,
    CashAlreadyOpen,
    DatabaseErrorItemNotFound,
    DuplicateProduct,
    InsufficientStock,
    PermissionDenied,
    ProductExpired,
    UserAlreadyCreated,
)
from bakery.backend.repository import DB
from guara.abstract_transaction import LOGGER, AbstractTransaction

# from bakery.backend.transactions import UserSession

# ==========================================================
# PRE-CONDITIONS
# ==========================================================


# Other
class UserSession:
    current_user: User | None = None

    def __init__(self):
        with open(SESSION_FILE, "r") as f:
            username = f.read()
            user = DB.get_user_by_name(username)
            if user and user.logged_in:
                UserSession.current_user = user


# =========================
# USERS
# =========================
class IsUserLoggedIn(AbstractTransaction):
    def do(self):
        user = UserSession().current_user
        if not user:
            raise BusinessError("Usuário não autenticado [User not logged in]")


class IsNotUserCreatedYet(AbstractTransaction):
    def do(self, name):
        try:
            self._driver.get_user_by_name(name)
        except DatabaseErrorItemNotFound:
            return
        raise UserAlreadyCreated


class IsNotDiscountHigh(AbstractTransaction):
    def do(self, discount):
        if discount > 0.2:
            raise Exception("Discount too high")  # noqa


class IsEnoughMoneyToBuy(AbstractTransaction):
    def do(self, money, card, sale_id, discount=0):
        sale = self._driver.get_sale_by_id(sale_id)
        for item in sale.items:
            product = self._driver.get_product_by_id(item.id)
            to_pay = product.price * item.quantity
            to_pay_with_discount = to_pay - (to_pay * discount)
        assert (
            money + card >= to_pay_with_discount
        ), f"Quantia não é suficiente para pagar a compra de R$ {to_pay_with_discount} [Insufficient money to buy]"


class AreValidValuesToSell(AbstractTransaction):
    def do(self, quantity=0):
        assert quantity > 0, "Quantidade precisa ser acima de 0 [Money need to be grater than 0]"


class AreValidValuesToPay(AbstractTransaction):
    def do(self, money=0, card=0):
        assert (
            money > 0 or card > 0
        ), "Quantia tem que ser acima de R$ 0.00 [Money need to be grater than 0]"


class AreValidValuesToRegistreProduct(AbstractTransaction):
    def do(self, price=0, minimum_stock=0):
        assert price > 0, "Preço tem que ser acima de R$ 0.00"
        assert minimum_stock > 0, "Estoque mínimo precisa ser acima de 0 [Minimum stock is 0]"


class AreValidValuesToCreateUser(AbstractTransaction):
    def do(self, name, secret, role):
        MAX_NAME_CHAR = 25
        MIN_SECRET_CHAR = 5
        assert name.strip() not in [
            None,
            "",
        ], "Nome do usuário não pode ser vazio [Name can not be empty]"
        assert (
            len(name) <= MAX_NAME_CHAR
        ), f"Nome do usuário não pode ter mais do que {MAX_NAME_CHAR} caracteres [Name exceeded maximum value]"
        assert secret not in [
            None,
            "",
        ], "Senha do usuário não pode ser vazia [Password can not be empty]"
        assert (
            len(secret) >= MIN_SECRET_CHAR
        ), f"Senha do usuário precisa ter {MIN_SECRET_CHAR} caracteres no mínimo"
        assert role.lower() in [
            "atendente",
            "gerente",
        ], "Função do usuário precisa ser Atendente ou Gerente [Ned to be manager or assistent]"


class IsRegistredProduct(AbstractTransaction):
    """
    name: str
    """

    def do(self, name=None, id_=None):
        if name:
            return self._driver.get_product_by_name(name)
        if id_:
            return self._driver.get_product_by_id(id_)


class HasNotRegistredProduct(AbstractTransaction):
    def do(self, name):
        for product in self._driver.list_products():
            if product.name.lower() == name.lower():
                raise DuplicateProduct("Produto já cadastrado [Product already registred]")


class HasNotCustomer(AbstractTransaction):

    def do(self, name, phone):
        if self._driver.get_customer_by_name(name):
            raise DuplicateProduct("Cliente já cadastrado [User already registred]")


class HasProductInStock(AbstractTransaction):
    def do(self, product_name, quantity):
        product = self._driver.get_product_by_name(product_name)
        if product.stock < quantity:
            raise InsufficientStock(f"Estoque insuficiente: {product.stock} [Low stock]")


class IsProductInValidExpirationDate(AbstractTransaction):
    def do(self, product_name=None, product_id=None):
        if product_name:
            product = self._driver.get_product_by_name(product_name)
        if product_id:
            product = self._driver.get_product_by_id(product_id)
        expired_batches = [
            batch
            for batch in self._driver.list_batches()
            if batch.product_id == product.id
            and batch.expiration_date < datetime.now(tz=timezone.utc).date()
        ]
        if expired_batches:
            raise ProductExpired("Produto vencido [Expired product]")


class IsValidRole(AbstractTransaction):
    def do(self, role):
        pass


class IsNotUserLoggedIn(AbstractTransaction):
    requires: ClassVar = [EntityIsNotNone]

    def do(self, username):
        user = self._driver.get_user_by_name(username)
        if user.logged_in is True:
            LOGGER.warning("Usuário já está logado [User already logged in]")


# =========================
# CASH REGISTER
# =========================


class IsOpenCashRegister(AbstractTransaction):
    def do(self):
        if self._driver.get_open_cash_register():
            return
        raise CashAlreadyClosed("Nenhum caixa aberto [Cash already closed]")


class IsNotOpenCashRegister(AbstractTransaction):
    def do(self):
        if self._driver.get_open_cash_register():
            raise CashAlreadyOpen("Já existe um caixa aberto [Cash already open]")


class IsManager(AbstractTransaction):
    def do(self):

        current_user = UserSession().current_user
        user = self._driver.get_user_by_name(current_user.name)
        if user and user.role.lower() != "gerente":
            raise PermissionDenied(
                "Acesso negado. Chame o gerente [Access denied. Call the manager.]"
            )
