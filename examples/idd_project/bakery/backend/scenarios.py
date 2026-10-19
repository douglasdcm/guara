from __future__ import annotations

from datetime import datetime

from bakery.backend import preconditons, transactions
from bakery.backend.helpers import IsGreatherThanOrEqualTo
from bakery.backend.repository import DB
from guara import LOGGER, it
from guara.transaction import Application


def scenario_login_user(username, secret):
    LOGGER.info("Login user")
    app = Application(DB)
    return (
        app.when(transactions.AuthenticateUser, username=username, secret=secret)
        .then(it.IsNotNone)
        .result
    )


def scenario_open_cash(initial):
    LOGGER.info("Opening cash register")
    app = Application(DB)
    (
        app.when(
            transactions.OpenCashRegister,
            initial_value=initial,
        ).expects(it.IsNotNone)
    )


def scenario_register_batch(product, quantity, expiration):
    app = Application(DB)
    (
        app.execute(
            transactions.RegisterBatch,
            product_name=product,
            quantity=quantity,
            expiration_date=datetime.strptime(expiration, "%Y-%m-%d").date(),
        )
    )


def scenario_close_cash(role):
    app = Application(DB)
    return app.execute(transactions.CloseCashRegister).result


def scenario_sangria_withdraw_cash(amount):
    app = Application(DB)
    (app.when(transactions.WithdrawCash, amount=amount).expects(it.IsEqualTo, amount))


def scenario_list_products():
    app = Application(DB)
    return app.when(transactions.ListProducts).expects(it.IsNotNone).result


def scenario_list_users():
    app = Application(DB)
    result = app.when(transactions.ListUsers).expects(it.IsNotNone).result
    app.dump_history("dump.json")
    return result


def scenario_list_customers():
    app = Application(DB)
    return app.when(transactions.ListCustomers).expects(it.IsNotNone).result


def scenario_list_sales():
    app = Application(DB)
    return app.when(transactions.ListSales).expects(it.IsNotNone).result


def scenario_sell(product_id, quantity, customer_id, delivery):
    app = Application(DB)
    try:
        result = (
            app.when(
                transactions.RegisterSale,
                # TODO convert items to product only
                items=[(product_id, quantity)],
                product_id=product_id,
                quantity=quantity,
                customer_id=customer_id,
                delivery=delivery,
            )
            .expects(it.IsNotNone)
            .result
        )
        if customer_id:
            app.execute(
                transactions.UpdateProductRating,
                items=[product_id],
                customer_id=customer_id,
            )
        return result
    except Exception as e:
        LOGGER.error(str(e))
        app.undo()
        raise


def scenario_pay_sale(sale_id, money, card, delivery):
    app = Application(DB)
    try:
        result = (
            app.when(transactions.Pay, money=money, card=card)
            .expects(it.IsNotNone)
            .result
        )
        return result
    except Exception as e:
        LOGGER.error(str(e))
        app.undo()
        raise


def scenario_recommend_products(customer_id, product_id):
    app = Application(DB)
    if customer_id:
        recommendations = (
            app.when(
                transactions.RecommendProduct,
                product_id=product_id,
                customer_id=customer_id,
            ).expects(it.IsNotNone)
        ).result
        if recommendations:
            for recommendation in recommendations:
                name = recommendation[0].name
                try:
                    app.given(
                        preconditons.HasProductInStock, product_name=name, quantity=1
                    )
                    return name
                except Exception:  # noqa
                    pass


def scenario_create_customer(name, phone):
    app = Application(DB)
    (
        app.and_(preconditons.HasNotCustomer, name=name, phone=phone).execute(
            transactions.RegisterCustomer, name=name, phone=phone
        )
    )


def scenario_add_stock(product, quantity):
    app = Application(DB)
    LOGGER.info("Adding product to stock")
    return (
        app.when(transactions.AddStock, product_name=product, quantity=quantity)
        .expects(IsGreatherThanOrEqualTo, quantity)
        .result
    )


def scenario_update_price(name, price):
    app = Application(DB)
    LOGGER.info("Updating price")
    (
        app.when(transactions.UpdateProductPrice, name=name, price=price).then(
            it.IsNotNone
        )
    )


def scenario_create_product(name, price, minimum_stock, weight):
    app = Application(DB)
    LOGGER.info("Creating product")
    (
        app.when(
            transactions.CreateProduct,
            name=name,
            price=price,
            minimum_stock=minimum_stock,
            sold_by_weight=weight,
        ).expects(it.IsTrue)
    )


def scenario_create_user(name, secret, role):
    app = Application(DB)
    LOGGER.info("Creating user")
    (
        app.when(
            transactions.CreateUser,
            name=name,
            secret=secret,
            role=role,
        ).expects(it.IsNotNone)
    )
