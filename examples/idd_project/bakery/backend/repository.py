from __future__ import annotations

from contextlib import contextmanager

from bakery.backend.database import SessionLocal
from bakery.backend.entities import (
    Batch,
    CashRegister,
    Customer,
    Product,
    Rating,
    Sale,
    SaleItem,
    User,
    Withdrawals,
)
from bakery.backend.exceptions import DatabaseErrorItemNotFound
from bakery.backend.models import (
    BatchModel,
    CashRegisterModel,
    CustomerModel,
    ProductModel,
    RatingModel,
    SaleItemModel,
    SaleModel,
    UserModel,
    WithdrawalsModel,
)


@contextmanager
def session_scope():
    session = SessionLocal()
    try:
        yield session
        session.commit()
        session.flush()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


class Repository:
    # =========================
    # PRODUCTS
    # =========================

    def _convert_to_product(self, model: ProductModel):
        return Product(
            id=model.id,
            name=model.name,
            price=model.price,
            minimum_stock=model.minimum_stock,
            sold_by_weight=model.sold_by_weight,
            stock=model.stock,
        )

    def add_product(self, product: Product):
        with session_scope() as session:
            model = ProductModel(
                name=product.name,
                price=product.price,
                minimum_stock=product.minimum_stock,
                sold_by_weight=product.sold_by_weight,
                stock=product.stock,
            )
            session.add(model)
            return self._convert_to_product(model)

    def update_product(self, product: Product):
        with session_scope() as session:
            model = session.query(ProductModel).filter_by(id=product.id).first()
            model.name = product.name
            model.price = product.price
            model.minimum_stock = product.minimum_stock
            model.sold_by_weight = product.sold_by_weight
            model.stock = product.stock
            session.flush()
            return self._convert_to_product(model)

    def get_product_by_name(self, name):
        with session_scope() as session:
            model = session.query(ProductModel).filter_by(name=name).first()
            if not model:
                raise DatabaseErrorItemNotFound("Produto não encontrado")
            return self._convert_to_product(model)

    def get_product_by_id(self, id_):
        with session_scope() as session:
            model = session.query(ProductModel).filter_by(id=id_).first()
            return self._convert_to_product(model)

    def list_products(self):
        with session_scope() as session:
            models = session.query(ProductModel).all()
            return [self._convert_to_product(model) for model in models]

    # =========================
    # USERS
    # =========================
    def _convert_to_user(self, model: UserModel):
        return User(
            id=model.id,
            name=model.username,
            role=model.role,
            secret=model.secret,
            logged_in=model.logged_in,
        )

    def list_users(self):
        with session_scope() as session:
            models = session.query(UserModel).all()
            return [self._convert_to_user(model) for model in models]

    def get_user_by_name(self, username):
        with session_scope() as session:
            model = session.query(UserModel).filter_by(username=username).first()
            if not model:
                raise DatabaseErrorItemNotFound(f"Usuário '{username}' não encontrado")
            return self._convert_to_user(model)

    def update_user_by_name(self, user: User):
        with session_scope() as session:
            model = session.query(UserModel).filter_by(username=user.name, role=user.role).first()
            model.logged_in = user.logged_in
            session.flush()
            return self._convert_to_user(model)

    def add_user(self, user: User):
        with session_scope() as session:
            user = UserModel(id=user.id, username=user.name, role=user.role, secret=user.secret)
            session.add(user)

    # =========================
    # CUSTOMERS
    # =========================

    def _convert_to_customer(self, model):
        return Customer(id=model.id, name=model.name, phone=model.phone)

    def add_customer(self, name, phone):
        with session_scope() as session:
            model = CustomerModel(name=name.lower(), phone=phone)
            session.add(model)
            return self._convert_to_customer(model)

    def get_customer_by_name(self, name):
        with session_scope() as session:
            model = session.query(CustomerModel).filter_by(name=name.lower()).first()
            if model:
                return self._convert_to_customer(model)

    def get_customer_by_id(self, id_):
        with session_scope() as session:
            model = session.query(CustomerModel).filter_by(id=id_).first()
            if model:
                return self._convert_to_customer(model)

    def list_customers(self):
        with session_scope() as session:
            models = session.query(CustomerModel).all()
            return [self._convert_to_customer(model) for model in models]

    # =========================
    # SALE ITEMS
    # =========================

    def _convert_to_sale_item(self, model: SaleItemModel):
        return SaleItem(
            id=model.id,
            product_id=model.product_id,
            quantity=model.quantity,
            unit_price=model.unit_price,
            sale_id=model.sale_id,
        )

    def _add_sale_item(self, sale: Sale, sale_item: SaleItem):
        with session_scope() as session:
            product = DB.get_product_by_id(sale_item.product_id)
            model = SaleItemModel(
                id=len(DB._list_sale_items()) + 1,
                product_id=sale_item.product_id,
                quantity=sale_item.quantity,
                sale_id=sale.id,
                unit_price=product.price,
            )
            session.add(model)
            return self._convert_to_sale_item(model)

    def _list_sale_items(self):
        with session_scope() as session:
            models = session.query(SaleItemModel).all()
            return [self._convert_to_sale_item(model) for model in models]

    # =========================
    # RATING
    # =========================

    def _convert_to_rating(self, model: RatingModel):
        return Rating(
            customer_id=model.customer_id,
            product_id=model.product_id,
            rating=model.rating,
        )

    def add_rating(self, customer_id, product_id):
        with session_scope() as session:
            model = RatingModel(
                customer_id=customer_id,
                product_id=product_id,
                rating=1,
            )
            session.add(model)
            return self._convert_to_rating(model)

    def get_rating(self, customer_id, product_id):
        with session_scope() as session:
            model = (
                session.query(RatingModel)
                .filter_by(customer_id=customer_id, product_id=product_id)
                .first()
            )
            if model:
                return self._convert_to_rating(model)

    def list_ratings(self):
        with session_scope() as session:
            models = session.query(RatingModel).all()
            return [self._convert_to_rating(model) for model in models]

    def update_rating(self, customer_id, product_id):
        with session_scope() as session:
            rating = DB.get_rating(customer_id, product_id)
            if rating:
                rating.rating += 1
                session.flush()
                return rating

    # =========================
    # SALES
    # =========================

    def _convert_to_sale(self, model: SaleModel, items: SaleItem):
        return Sale(
            items=items,
            id=model.id,
            customer_id=model.customer_id,
            delivery_address=model.delivery_address,
        )

    def get_sale_by_id(self, id_):
        with session_scope() as session:
            sale = session.query(SaleModel).filter_by(id=id_).first()
            items = session.query(SaleItemModel).filter_by(sale_id=sale.id).all()
            return self._convert_to_sale(sale, items)

    def add_sale(self, sale: Sale):
        with session_scope() as session:
            model = SaleModel(
                total=len(sale.items),
                customer_id=sale.customer_id,
                delivery_address=sale.delivery_address,
            )
            session.add(model)
            for item in sale.items:
                self._add_sale_item(sale, item)
            return self._convert_to_sale(model, sale.items)

    def remove_sale(self, sale: Sale):
        pass

    def list_sales(self) -> list[Sale]:
        with session_scope() as session:
            sales = []
            sale_items = []
            sale_models = session.query(SaleModel).all()
            for sale_model in sale_models:
                sale_item_models = (
                    session.query(SaleItemModel).filter_by(sale_id=sale_model.id).all()
                )
                for sale_item_model in sale_item_models:
                    sale_item = self._convert_to_sale_item(sale_item_model)
                    sale_items.append(sale_item)
                sale_ = self._convert_to_sale(sale_model, sale_items)
                sales.append(sale_)
                sale_items = []
            return [sale for sale in sales]

    # =========================
    # CASH
    # =========================

    def _convert_to_cash_register(self, model: CashRegisterModel):
        return CashRegister(
            id=model.id,
            opened_by=model.opened_by,
            initial_value=model.initial_value,
            closed_at=model.closed,
            closed=model.closed,
        )

    def _get_cash_register(self):
        with session_scope() as session:
            model = session.query(CashRegisterModel).first()
            if model:
                return self._convert_to_cash_register(model)

    def get_open_cash_register(self):
        with session_scope() as session:
            model = session.query(CashRegisterModel).filter_by(closed=False).first()
            if model:
                return self._convert_to_cash_register(model)

    def open_cash_register(self, initial):
        with session_scope() as session:
            cash = self._get_cash_register()
            if not cash:
                model = CashRegisterModel(initial_value=initial, closed=False)
                session.add(model)
                return self._convert_to_cash_register(model)
            if cash.closed is False:
                return cash
            else:
                model = session.query(CashRegisterModel).first()
                model.closed = False
                session.flush()
                return self._convert_to_cash_register(model)

    def close_cash_register(self):
        with session_scope() as session:
            cash = self.get_open_cash_register()
            if cash:
                model = session.query(CashRegisterModel).first()
                model.closed = True
                session.flush()
                return self._convert_to_cash_register(model)
            return self._get_cash_register()

    # =========================
    # Withdrawal
    # =========================
    def _convert_to_withdrawl(self, model: WithdrawalsModel):
        return Withdrawals(
            id=model.id,
            cash_register_id=model.cash_register_id,
            withdrawal=model.withdrawal,
        )

    def add_withdrawal(self, withdrawal):
        with session_scope() as session:
            cash_register = self.get_open_cash_register()
            model = WithdrawalsModel(cash_register_id=cash_register.id, withdrawal=withdrawal)
            session.add(model)
            return self._convert_to_withdrawl(model)

    def list_withdrawals(self):
        with session_scope() as session:
            models = session.query(WithdrawalsModel).all()
            return [self._convert_to_withdrawl(model).withdrawal for model in models]

    # =========================
    # BATCH
    # =========================

    def add_batch(self, product_id, quantity, expiration_date):
        with session_scope() as session:
            model = BatchModel(
                quantity=quantity,
                expiration_date=expiration_date,
                product_id=product_id,
            )
            session.add(model)
            return self._convert_to_batch(model)

    def _convert_to_batch(self, model):
        return Batch(
            product_id=model.id,
            quantity=model.quantity,
            expiration_date=model.expiration_date,
        )

    def list_batches(self):
        with session_scope() as session:
            models = session.query(BatchModel).all()
            return [self._convert_to_batch(model) for model in models]


DB = Repository()
