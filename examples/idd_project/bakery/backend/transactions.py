from typing import ClassVar

from surprise import dump

from bakery.backend import preconditons
from bakery.backend.constants import SESSION_FILE
from bakery.backend.entities import Product, Sale, SaleItem, User
from bakery.backend.exceptions import BusinessError
from bakery.backend.preconditons import IsManager, IsUserLoggedIn
from bakery.backend.repository import Repository
from bakery.backend.utils import get_total_sales
from guara.abstract_transaction import AbstractTransaction

# ==========================================================
# TRANSACTIONS
# ==========================================================


class CreateUser(AbstractTransaction):
    requires: ClassVar = [
        preconditons.AreValidValuesToCreateUser,
        preconditons.IsNotUserCreatedYet,
    ]

    def __init__(self, driver=None):
        super().__init__(driver)
        self._driver: Repository

    def do(self, name, secret, role):
        user = User(
            id=len(self._driver.list_users()) + 1,
            name=name,
            secret=secret,
            role=role,
        )
        self._driver.add_user(user)
        return self._driver.get_user_by_name(name)


class CreateProduct(AbstractTransaction):
    requires: ClassVar = [
        preconditons.IsUserLoggedIn,
        preconditons.IsManager,
        preconditons.AreValidValuesToRegistreProduct,
        preconditons.HasNotRegistredProduct,
    ]

    def __init__(self, driver=None):
        super().__init__(driver)
        self._driver: Repository

    def do(self, name, price, minimum_stock, sold_by_weight=False):
        product = Product(
            id=len(self._driver.list_products()) + 1,
            name=name,
            price=price,
            minimum_stock=minimum_stock,
            sold_by_weight=sold_by_weight,
        )
        self._driver.add_product(product)
        return True


class UpdateProductPrice(AbstractTransaction):
    requires: ClassVar = [
        preconditons.IsUserLoggedIn,
        preconditons.IsManager,
        preconditons.IsRegistredProduct,
    ]

    def __init__(self, driver=None):
        super().__init__(driver)
        self._driver: Repository

    def do(self, name, price):
        product = self._driver.get_product_by_name(name)
        product.price = price
        return self._driver.update_product(product)


class AddStock(AbstractTransaction):
    requires: ClassVar = [
        preconditons.IsUserLoggedIn,
        preconditons.IsManager,
        preconditons.IsRegistredProduct,
    ]

    def __init__(self, driver=None):
        super().__init__(driver)
        self._driver: Repository

    def do(self, product_name, quantity):
        product = self._driver.get_product_by_name(product_name)
        product.stock += quantity
        product = self._driver.update_product(product)
        return product.stock


class RegisterBatch(AbstractTransaction):
    requires: ClassVar = [
        preconditons.IsUserLoggedIn,
        preconditons.IsRegistredProduct,
    ]

    def __init__(self, driver=None):
        super().__init__(driver)
        self._driver: Repository

    def do(self, product_name, quantity, expiration_date):
        product = self._driver.get_product_by_name(product_name)
        product.stock += quantity
        batch = self._driver.add_batch(product.id, quantity, expiration_date)
        self._driver.update_product(product)
        return batch


class RegisterCustomer(AbstractTransaction):
    def __init__(self, driver=None):
        super().__init__(driver)
        self._driver: Repository

    def do(self, name, phone):
        return self._driver.add_customer(name, phone)


class RegisterSale(AbstractTransaction):
    requires: ClassVar = [
        preconditons.IsUserLoggedIn,
        preconditons.IsOpenCashRegister,
        preconditons.AreValidValuesToSell,
        preconditons.IsRegistredProduct,
        # # It is not necessary to check the stock given that the customer is in front of the
        # # cashier with all the products in hand
        # # .and_(preconditons.HasProductInStock, product_name=product, quantity=quantity)
        preconditons.IsProductInValidExpirationDate,
    ]

    def __init__(self, driver=None):
        super().__init__(driver)
        self._driver: Repository

    def do(self, items, quantity, product_id, customer_id=None, delivery=None):
        sale_items: list[SaleItem] = []

        for _product_id, _quantity in items:
            product = self._driver.get_product_by_id(_product_id)
            sale_items.append(
                SaleItem(
                    len(self._driver._list_sale_items()) + 1,
                    len(self._driver.list_sales()) + 1,
                    product.id,
                    _quantity,
                    product.price,
                )
            )

        if customer_id:
            customer_id = self._driver.get_customer_by_id(customer_id).id

        sale = Sale(
            id=len(self._driver.list_sales()) + 1,
            items=sale_items,
            customer_id=customer_id,
            delivery_address=delivery,
        )

        self._driver.add_sale(sale)
        for _product_id, _quantity in items:
            product = self._driver.get_product_by_id(_product_id)
            product.stock -= _quantity
            self._driver.update_product(product)

        if customer_id:
            for item in sale_items:
                rating = self._driver.get_rating(customer_id, item.product_id)
                if rating:
                    self._driver.update_rating(customer_id, item.product_id)
                    continue
                self._driver.add_rating(customer_id, item.product_id)
        return sale

    def undo(self):
        pass


class Pay(AbstractTransaction):
    requires: ClassVar = [
        preconditons.IsUserLoggedIn,
        preconditons.IsOpenCashRegister,
        preconditons.AreValidValuesToPay,
        preconditons.IsEnoughMoneyToBuy,
    ]

    def __init__(self, driver=None):
        super().__init__(driver)
        self._driver: Repository

    def do(self, money=None, card=None):
        return True


class RecommendProduct(AbstractTransaction):
    def __init__(self, driver=None):
        super().__init__(driver)
        self._driver: Repository

    def do(self, product_id, customer_id):
        top_n = 5
        _, model = dump.load("./surprise_model.dump")
        scores = []
        for product in self._driver.list_products():
            if product.id != product_id:
                pred = model.predict(customer_id, product_id)
                scores.append((product, pred.est))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_n]


class UpdateProductRating(AbstractTransaction):
    def __init__(self, driver=None):
        super().__init__(driver)
        self._driver: Repository

    def do(self, items, customer_id=None):
        customer_id = None
        if customer_id:
            customer_id = self._driver.get_customer_by_id(customer_id).id
        else:
            return True

        item = {
            "product_id": None,
            "customer_id": None,
        }

        sale_items = []

        for product_id in items:
            product = self._driver.get_product_by_id(product_id)
            sale_items.append(
                {
                    "product_id": product.id,
                    "customer_id": customer_id,
                }
            )

        for item in sale_items:
            customer_id = item["customer_id"]
            product_id = item["product_id"]
            rating = self._driver.get_rating(customer_id, product_id)
            if rating:
                self._driver.update_rating(customer_id, product_id)
                continue
            self._driver.add_rating(customer_id, product_id)
        return True


class OpenCashRegister(AbstractTransaction):
    requires: ClassVar = [
        preconditons.IsUserLoggedIn,
        preconditons.IsNotOpenCashRegister,
    ]
    ensures: ClassVar = [preconditons.IsOpenCashRegister]

    def __init__(self, driver=None):
        super().__init__(driver)
        self._driver: Repository

    def do(self, initial_value):
        return self._driver.open_cash_register(initial_value)


class WithdrawCash(AbstractTransaction):
    requires: ClassVar = [
        preconditons.IsUserLoggedIn,
        preconditons.IsOpenCashRegister,
    ]

    def __init__(self, driver=None):
        super().__init__(driver)
        self._driver: Repository

    def do(self, amount):
        return self._driver.add_withdrawal(amount).withdrawal


class CloseCashRegister(AbstractTransaction):
    requires: ClassVar = [
        preconditons.IsUserLoggedIn,
        preconditons.IsManager,
        preconditons.IsOpenCashRegister,
    ]

    def __init__(self, driver=None):
        super().__init__(driver)
        self._driver: Repository

    def do(self):
        self._driver.close_cash_register()
        total_sales = get_total_sales()
        return {
            "total_sales": total_sales,
            "withdrawals": sum(self._driver.list_withdrawals()),
        }


class AuthenticateUser(AbstractTransaction):
    requires: ClassVar = [
        preconditons.IsNotUserLoggedIn,
    ]

    def __init__(self, driver=None):
        super().__init__(driver)
        self._driver: Repository

    def do(self, username, secret) -> User:
        user = self._driver.get_user_by_name(username)
        if not user or user.secret != secret:
            raise BusinessError("Credenciais inválidas [Invalid secret]")
        # saves session locally
        with open(SESSION_FILE, "w") as f:
            # TODO save a token based on user data
            f.write(username)
        user.logged_in = True
        user = self._driver.update_user_by_name(user)
        return user


class ListProducts(AbstractTransaction):
    requires: ClassVar = [
        preconditons.IsUserLoggedIn,
        preconditons.IsOpenCashRegister,
    ]

    def __init__(self, driver=None):
        super().__init__(driver)
        self._driver: Repository

    def do(self):
        return self._driver.list_products()


class ListUsers(AbstractTransaction):
    requires: ClassVar = [
        preconditons.IsUserLoggedIn,
        preconditons.IsManager,
    ]

    def __init__(self, driver=None):
        super().__init__(driver)
        self._driver: Repository

    def do(self):
        return self._driver.list_users()


class ListCustomers(AbstractTransaction):
    requires: ClassVar = [IsUserLoggedIn, IsManager]

    def __init__(self, driver=None):
        super().__init__(driver)
        self._driver: Repository

    def do(self):
        return self._driver.list_customers()


class ListSales(AbstractTransaction):
    requires: ClassVar = [
        preconditons.IsUserLoggedIn,
        preconditons.IsManager,
    ]

    def __init__(self, driver=None):
        super().__init__(driver)
        self._driver: Repository

    def do(self):
        return self._driver.list_sales()
